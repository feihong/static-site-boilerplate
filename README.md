# Static Site Boilerplate

Download:

```
curl -sL https://github.com/feihong/static-site-boilerplate/archive/master.tar.gz | tar xz
```

Rename the `static-site-boilerplate` directory to whatever you want, and cd into it. Then run the following at the command line:

```
pip install virtualenvwrapper
mkvirtualenv static-site
pip install -r requirements.txt
```

There is a minor amount of configuration you'll have to do inside `tasks.py`. At minimum, you will want to change the SITE variable.

## Commands

| **Command** | **Description** |
|-------------|-----------------|
| `inv serve` | Serve the site at localhost:8000 |
| `inv build` | Build the site |
| `inv publish` | Publish the site to GitHub Pages |

## Install Stylus support

If you want to use Stylus, you must first install Node.js.

On Mac (assuming you have Homebrew):

```
brew install node
```

On Linux, you can run something like this (you may want to change the 6.2.0 to whatever the latest version number is):

```
wget -O nodejs.tar.xz https://nodejs.org/dist/v6.2.0/node-v6.2.0-linux-x64.tar.xz
sudo tar -C /usr/local --strip-components 1 -xJf nodejs.tar.xz
```

Once Node.js has been installed, run this to install Stylus:

```
npm install stylus -g
```
