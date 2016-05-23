import os.path as op
import re
from pathlib import Path, PurePath
from mako.template import Template
from mako.lookup import TemplateLookup
import bottle
import yaml
from invoke import run, task


SITE = '/static-site-boilerplate/'
IMPORTS = [
    'from filters import markdown, rst'
]

lookup = TemplateLookup(directories=['templates'])

bottle.debug(True)
app = bottle.Bottle()

if SITE != '/':
    @app.route('/')
    def index():
        return '<a href="%s">Go to site</a>' % SITE


@app.route(SITE)
@app.route(SITE + '<path:path>')
def page(path=''):
    file_ = get_file(path)
    if not file_.endswith('.html'):
        return bottle.static_file(path, root='site')
    return generate(file_)


@task
def serve():
    from livereload import Server
    from livereload.watcher import Watcher
    watcher = Watcher()
    watcher.watch('site', ignore=lambda p: p.endswith('.babel'))
    watcher.watch('templates')
    server = Server(app, watcher)
    server.serve(port=8000)


@task
def build():
    clean()
    for src in Path('site').rglob('*?.*'):
        dest = Path('build') / src.relative_to('site')
        print dest
        copy_or_generate(src, dest)


@task
def clean():
    if op.isdir('build'):
        run('rm -rf build/*')


@task
def publish():
    build()
    run('ghp-import -n -p build')


def get_file(path):
    result = op.join('site', path)
    if op.isfile(result):
        return result
    if op.isdir(result) and op.isfile(op.join(result, 'index.html')):
        return op.join(result, 'index.html')
    return 'site/404.html'


def get_slug(path):
    if path == 'site/index.html':
        return ''
    elif path.endswith('index.html'):
        return str(PurePath(path).parent.name)
    else:
        return str(PurePath(path).stem)


def generate(path):
    with open(path) as fp:
        markup = fp.read()
        match = re.search(r'\n={3,}\n', markup)
        if match:
            start, end = match.span()
            data = yaml.load(markup[0:start])
            markup = markup[end:]
        template = Template(markup, lookup=lookup, imports=IMPORTS)
        return template.render(site=SITE, slug=get_slug(path), **data)


def copy_or_generate(src, dest):
    import shutil
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix == '.html':
        with dest.open('w') as fp:
            fp.write(generate(str(src)))
    else:
        shutil.copy(str(src), str(dest))
