from functools import cache

import nh3
from markdown_it import MarkdownIt

ALLOWED_TAGS = {
    "p",
    "br",
    "hr",
    "em",
    "strong",
    "code",
    "pre",
    "blockquote",
    "ul",
    "ol",
    "li",
    "a",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
}
ALLOWED_ATTRIBUTES = {"a": {"href"}, "div": {"role", "aria-level"}}
LINK_REL = "ugc nofollow noopener"


def _only_web_links(url):
    return url.lower().startswith(("http://", "https://"))


def _heading_open(base):
    def render(tokens, index, options, env):
        level = int(tokens[index].tag[1]) + base
        if level <= 6:
            return f"<h{level}>"
        return f'<div role="heading" aria-level="{level}">'

    return render


def _heading_close(base):
    def render(tokens, index, options, env):
        level = int(tokens[index].tag[1]) + base
        return f"</h{level}>" if level <= 6 else "</div>"

    return render


def _image_as_alt_text(renderer):
    def render(tokens, index, options, env):
        text = renderer.renderInlineAsText(tokens[index].children, options, env)
        return nh3.clean(text, tags=set())

    return render


@cache
def _markdown(heading_base):
    md = MarkdownIt("commonmark", {"html": False})
    md.validateLink = _only_web_links
    md.renderer.rules["image"] = _image_as_alt_text(md.renderer)
    md.renderer.rules["heading_open"] = _heading_open(heading_base)
    md.renderer.rules["heading_close"] = _heading_close(heading_base)
    return md


def render(source, heading_base=1):
    """Render CommonMark source as sanitized HTML (data model, section 2.3.1).

    Headings are shifted by heading_base so that a testimony never repeats the
    page's h1. Raw HTML is disabled, images show their alt text, and only http
    and https links are kept, with rel="ugc nofollow noopener".
    """
    html = _markdown(heading_base).render(source)
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        link_rel=LINK_REL,
        url_schemes={"http", "https"},
    )


def plain_text(source):
    return nh3.clean(render(source), tags=set()).strip()
