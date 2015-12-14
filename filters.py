from markdown2 import markdown
from docutils.core import publish_parts


def rst(s):
    result = publish_parts(s, writer_name="html")["html_body"]
    # Get rid of the outer div.
    return result[22:-7]
