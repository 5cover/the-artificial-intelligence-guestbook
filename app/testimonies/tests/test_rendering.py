from testimonies.rendering import plain_text, render


def test_headings_are_shifted_below_the_page_heading():
    assert render("# Title") == "<h2>Title</h2>"


def test_headings_beyond_level_six_keep_their_level_as_aria():
    assert render("###### Deep") == '<div role="heading" aria-level="7">Deep</div>'


def test_raw_html_is_shown_as_text():
    html = render("<b>bold</b> and <script>alert(1)</script>")
    assert "<script" not in html
    assert "&lt;b&gt;bold&lt;/b&gt;" in html


def test_images_show_their_alternative_text_only():
    html = render("![a sunset](https://example.org/sunset.png)")
    assert "<img" not in html
    assert "a sunset" in html


def test_web_links_are_kept_with_safe_rel():
    html = render("[ok](https://example.org/a)")
    assert '<a href="https://example.org/a" rel="ugc nofollow noopener">ok</a>' in html


def test_other_schemes_are_shown_as_text():
    html = render("[mail](mailto:someone@example.org)")
    assert "<a " not in html
    assert "mail" in html


def test_script_urls_are_never_links():
    html = render("[click](javascript:alert(1))")
    assert "<a " not in html
    assert "href" not in html


def test_plain_text_drops_all_markup():
    assert (
        plain_text("Some *emphasis* and a [link](https://example.org).")
        == "Some emphasis and a link."
    )
