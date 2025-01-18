TAG_BLOCKLIST = [
    "ol.references",
    ".reference",
    "link",
    "style",
    "img",
    "aside",
    "table",
    "br",
    "span.mw-ext-cite-error",
    "div.thumbinner",
    "div.gallerytext",
    "div.archwiki-template-meta-related-articles-start",
    "div.tright",
    "div.plainlist",
    "div.gametabs",
    ".noprint",
    "span#w4g_rb_area-1",
    "p.caption",
]


DEFAULT_PARAMS: dict[str, str | int] = {
    "format": "json",
    "action": "query",
    "formatversion": 2,
}
