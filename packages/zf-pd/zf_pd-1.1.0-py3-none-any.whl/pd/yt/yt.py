from playwright.sync_api import sync_playwright

from click import group, option
from loguru import logger
from playwright.sync_api import sync_playwright
from perse import reduce_html_content, extract_content_tag


@group(name='yt', help="YouTube utilities")
def yt():
    pass


@yt.command(help="Extract YouTube video details")
@option('-l', '--link', type=str, required=True, prompt=True,
        help="Link to the YouTube video")
def extract(link: str):
    logger.debug("yt extract")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(link)

        page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 100;
                    const timer = setInterval(() => {
                        const scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if (totalHeight >= scrollHeight) {
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)

        exclude_tags = {"script", "style", "svg", "iframe", "noscript", "form", "link", "meta"}
        html_content = page.content()

        browser.close()

        reduced_html_content = reduce_html_content(content=html_content, exclude_tags=exclude_tags)

        shorts_links_element = extract_content_tag(
            content=reduced_html_content,
            attribute="href",
            pattern="/shorts/"
        )

        shorts_elems = shorts_links_element.find_all("div", class_="ShortsLockupViewModelHostOutsideMetadata")

        with open("extracted_shorts_elements.html", "w") as f:
            for shorts_elem in shorts_elems:
                f.write(shorts_elem.prettify())