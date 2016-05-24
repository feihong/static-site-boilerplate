import os.path as op
import re
from pathlib2 import Path
from mako.template import Template
from mako.lookup import TemplateLookup
import bottle
from pyjade.ext.mako import preprocessor as jade2mako
from invoke import run, task
from filters import markdown, rst


SITE = '/static-site-boilerplate/'
IMPORTS = [
    'from filters import markdown, rst'
]
FORMATS = ('.html', '.rst', '.md', '.jade')

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
    if file_ is None:
        with open('site/404.html') as fp:
            return fp.read()

    if file_.suffix in FORMATS:
        return generate(file_)

    return bottle.static_file(path, root='site')



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
    result = Path('site') / path
    if result.is_file():
        return result

    for format in FORMATS:
        index_file = result / ('index' + format)
        if result.is_dir() and index_file.is_file():
            return index_file
    return None


def get_slug(path):
    if str(path) == 'site/index.html':
        return 'home'
    elif path.stem == 'index':
        return str(path.parent.name)
    else:
        return str(path.stem)


def split_markup(markup):
    """
    Given some markup, return a tuple containing the decoded data and the
    template code.

    """
    import yaml

    match = re.search(r'\n={3,}\n', markup)
    if match:
        start, end = match.span()
        data = yaml.load(markup[0:start])
        template_code = markup[end:]
    else:
        data = None
        template_code = markup

    return data, template_code


def generate(path):
    data, template_code = split_markup(path.read_text())
    data.update(site=SITE, slug=get_slug(path))
    content = render(template_code, data)
    if path.suffix == '.rst':
        html = rst(content)
        return render('<%inherit file="base.html" />\n' + html, data)
    if path.suffix == '.md':
        html = markdown(content)
        return render('<%inherit file="base.html" />\n' + html, data)
    return content


def render(template_code, data):
    template = Template(template_code, lookup=lookup, imports=IMPORTS)
    return template.render(**data)


def copy_or_generate(src, dest):
    import shutil
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix in FORMATS:
        dest = dest.parent / (dest.stem + '.html')
        with dest.open('w') as fp:
            fp.write(generate(src))
    else:
        shutil.copy(str(src), str(dest))
