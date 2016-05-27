title: Markdown

===

This page was written in [Markdown](https://daringfireball.net/projects/markdown/).

Fenced code blocks
------------------

```python
@app.route(SITE)
@app.route(SITE + '<path:path>')
def page(path=''):
    file_ = get_file(path)
    if file_ is None:
        with open('site/404.html') as fp:
            return fp.read()

    if file_.suffix in PAGE_FORMATS:
        return render_page(file_)

    if file_.suffix == '.styl':
        bottle.response.content_type = 'text/css'
        return render_stylesheet(file_)

    return bottle.static_file(path, root='site')
```

Blockquote
----------

> 每当音乐响起
>
> 总是身不由己
>
> 走进梦幻的世界
>
>一切变得很神奇

Reference links
---------------

I really like programming in [Python][python]. I'm not a big fan of [Ruby][ruby], though. I can tell you that [Python][] never lets me down!

[python]: https://python.org
[ruby]: https://ruby-lang.org

Images
------

![A fun picture I drew](http://67.media.tumblr.com/71313cc8d41737c0ec31d957fe9dfb61/tumblr_mi2on7vxWZ1rvuj8do1_500.png)

Miscellaneous
-------------

Email address:

<first.last@address.com> (view the source to see that address is entity-encoded)

Horizontal rule:

-----------------------------

Line breaks:

Awkward at weddings  
Godzilla only came for  
The free food and drinks

<div style='font-size: 0.7em; color: gray'>Source: <a href='http://godzillahaiku.tumblr.com/post/625840712/72'>Godzilla Haiku</a></div>
