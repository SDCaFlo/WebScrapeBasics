import asyncio
import sys
from playwright.async_api import async_playwright
import xml.etree.ElementTree as ET

async def get_sitemaps_url(url, page):
    """Pasamos una URL y un browser para extraer la URL de sitemaps"""
    robots = url+"robots.txt"
    await page.goto(robots)
    content = await page.text_content("body")
    if content:
    # Filtrar líneas que contienen "Sitemap:"
        sitemaps_list= [line.split(": ", 1)[1] for line in content.splitlines() if line.lower().startswith("sitemap:")]
    return sitemaps_list

async def get_all_urls(sitemap, browser):
    page = await browser.new_page()
    await page.goto(sitemap)
    #content = await page.content()
    xml_content = await page.evaluate(""" 
        async () => {
                const response = await fetch(window.location.href);
                return await response.text();
            }
        """)
    tree = ET.fromstring(xml_content)

    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    titles = tree.findall('.//ns:loc', namespace)

    for title in titles:
        print(title.text)

async def run(url):
    async with async_playwright() as p:
        
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # await page.goto(url)
        # await page.screenshot(path=r".\screenshots\screenshot.png")
        sitemaps = await get_sitemaps_url(url, page)
        
        for sitemap in sitemaps:
            await page.goto(sitemap)
            await page.screenshot(path=r".\screenshots\screenshot.png")
            await get_all_urls(sitemap, browser)

        await browser.close()




if __name__ == "__main__":
    url = sys.argv[1]
    print(url)
    asyncio.run(run(url))  # Run the async function