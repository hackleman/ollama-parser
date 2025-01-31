from scraper.scrape import scrape_website_local
from parsers.ollama import parse_with_model
from scraper.utils import flatten_list
from models.encoder import CustomEncoder
import json
import time
import asyncio
import concurrent.futures

async def main():
    url = "https://www.aa.org/find-aa/north-america"
    print(f"Scraping the url: {url}")

    result = scrape_website_local(url)
    meeting_content_list = flatten_list(list(result.values()))

    result = []

    for i in range(0, len(meeting_content_list), 9):
        batch = '\n\n'.join(meeting_content_list[i:i + 9])
        print(f"Processing  batch {i / 9 + 1} of {len(meeting_content_list) // 9}")
        meeting_list = await parse_with_timeout(i, batch)

        with open('output.json', 'a') as f:
            json.dump(meeting_list.meetings, f, indent=4, cls=CustomEncoder)
        result.extend(meeting_list.meetings)

    print(f"finished processing {len(meeting_content_list) // 9 } batches")


async def parse_with_timeout(i, batch):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            loop = asyncio.get_running_loop()
            future = loop.run_in_executor(executor, parse_with_model, batch)
            meeting_list = await asyncio.wait_for(future, timeout=60)
            return meeting_list
        except asyncio.TimeoutError:
            print(f"Ollama call timed out for batch: {i}")
            return []
    
if __name__ == "__main__":
    asyncio.run(main())