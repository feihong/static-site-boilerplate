import markdown2
from docutils.core import publish_parts


def rst(s):
    result = publish_parts(s, writer_name="html")["html_body"]
    # Get rid of the outer div.
    return result[22:-7]


def markdown(s):
    return markdown2.markdown(s, extras=['fenced-code-blocks'])
