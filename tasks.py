import os.path as op
import re
from pathlib2 import Path
from mako.template import Template
from mako.lookup import TemplateLookup
import bottle
from invoke import run, task
from filters import markdown, rst


SITE = '/static-site-boilerplate/'
IMPORTS = [
    'from filters import markdown, rst'
]
PAGE_FORMATS = ('.html', '.rst', '.md', '.jade')

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

    if file_.suffix in PAGE_FORMATS:
        return render_page(file_)

    if file_.suffix == '.scss':
        bottle.response.content_type = 'text/css'
        return render_stylesheet(file_)

    return bottle.static_file(path, root='site')



@task
def serve():
    from livereload import Server
    from livereload.watcher import Watcher
    watcher = Watcher()
    watcher.watch('site')
    watcher.watch('templates')
    server = Server(app, watcher)
    server.serve(port=8000)


@task
def build():
    clean()
    for src in Path('site').rglob('*?.*'):
        dest_dir = Path('build') / src.relative_to('site').parent
        dest_file = copy_or_generate(src, dest_dir)
        print dest_file

@task
def clean():
    if op.isdir('build'):
        run('rm -rf build/*')


@task
def publish():
    build()
    run('ghp-import -n -p build')


def get_file(path):
    filepath = Path('site') / path
    if filepath.is_file():
        return filepath

    for format in PAGE_FORMATS:
        index_file = filepath / ('index' + format)
        if filepath.is_dir() and index_file.is_file():
            return index_file

    if filepath.suffix == '.css':
        style_file = filepath.parent / (filepath.stem + '.scss')
        if style_file.exists():
            return style_file

    return None


def get_slug(path):
    if str(path) == 'site/index.html':
        return '/'
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
        data = {}
        template_code = markup

    return data, template_code


def render_page(path):
    data, template_code = split_markup(path.read_text())
    data.update(site=SITE, slug=get_slug(path))

    if path.suffix == '.jade':
        return render_jade(template_code, data)

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


def render_jade(template_code, data):
    from pyjade.ext.mako import preprocessor
    mako_code = preprocessor(template_code)
    index = mako_code.index('%>') + 2
    preamble = mako_code[:index]
    body = mako_code[index:]
    return render(
        preamble + '\n<%inherit file="base.html" />\n' + body,
        data)


def render_stylesheet(path):
    import sass
    return sass.compile(filename=str(path))


def copy_or_generate(src, dest_dir):
    import shutil
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
    if src.suffix in PAGE_FORMATS:
        dest = dest_dir / (src.stem + '.html')
        with dest.open('w') as fp:
            fp.write(render_page(src))
        return dest
    else:
        shutil.copy(str(src), str(dest_dir))
        return dest_dir / src.name
