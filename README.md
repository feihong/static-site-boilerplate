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

## Commands

| **Command** | **Description** |
|-------------|-----------------|
| `invoke serve` | Serve the site at localhost:8000 |
| `ionic build` | Build the site |
| `ionic publish` | Publish the site to GitHub Pages |
