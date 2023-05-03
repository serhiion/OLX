import asyncio
import re

from lxml import html

from server import create_advertisement, get_ads_urls
from olxScraper import CATEGORY_URL, HOST_NAME
from olxScraper import make_request


class OlxScraper(object):
    @staticmethod
    def parse_advertisement(page_content: str) -> list[str]:
        return [f'{HOST_NAME}{url}' for url in html.fromstring(page_content).xpath('.//a[@class="css-rc5s2u"]/@href')]

    async def get_advertisement_urls(self, page_number: int, advertisements: list) -> None:
        page_content = await make_request(CATEGORY_URL.format(page=page_number))
        advertisements.extend(self.parse_advertisement(page_content))

    async def get_advertisement_detail(self, url: str):
        page_content = await make_request(url)
        self.parse_advertisement_detail(page_content, url)

    @staticmethod
    def parse_advertisement_detail(page_content: str, url: str):
        try:
            ad_tree = html.fromstring(page_content)

            olx_id = int(ad_tree.xpath('.//span[@class="css-12hdxwj er34gjf0"]/text()')[1])
            ad_name = ad_tree.xpath('.//h1[@data-cy="ad_title"]/text()')[0]

            raw_price = ad_tree.xpath('.//h3[@class="css-ddweki er34gjf0"]/text()')[0]
            ad_price = int(re.findall(r'([0-9 ]+)', raw_price)[0].replace(' ', ''))
            ad_currency = re.findall(r'([$грн.€]+)', raw_price)[0]

            ad_image = ad_tree.xpath('.//img/@src')[0]
            ad_author_name = ad_tree.xpath('.//h4[@class="css-1lcz6o7 er34gjf0"]/text()')[0]

            create_advertisement(olx_id, ad_name, ad_price, ad_currency, ad_image, ad_author_name, url)
        except Exception as e:
            print(e)
            print(url)

    async def main(self):
        pages = []
        advertisements = []
        for page_number in range(1, 7):
            pages.append(self.get_advertisement_urls(page_number, advertisements))
        await asyncio.gather(*pages)

        advertisements = set(advertisements).difference(get_ads_urls())
        if len(advertisements) > 0:
            advertisements_details = []
            for advertisement in advertisements:
                advertisements_details.append(self.get_advertisement_detail(advertisement))

            await asyncio.gather(*advertisements_details)
            advertisements_details.clear()


if __name__ == '__main__':
    asyncio.run(OlxScraper().main())
