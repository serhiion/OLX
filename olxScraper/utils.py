from aiohttp import ClientSession

from olxScraper import HEADERS


async def make_request(url: str) -> str:
    async with ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:
            return await response.text()
