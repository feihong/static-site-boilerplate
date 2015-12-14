# Static Site Boilerplate

Download:

```
curl -sL https://github.com/feihong/static-site-boilerplate/archive/master.tar.gz | tar xz
```

Rename the `static-site-boilerplate` directory to whatever you want, and cd into it. Make sure you've already installed [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper/), and run the following:

```
mkvirtualenv static-site
pip install -r requirements.txt
```

There is a minor amount of configuration you'll have to do inside `tasks.py`.

To serve the site:

```
invoke serve
```

To build the site:

```
invoke build
```

To publish the site to GitHub Pages:

```
invoke publish
```
static-site-boilerplate
