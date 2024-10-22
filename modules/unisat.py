from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext
import asyncio

import logging

logger = logging.getLogger(__name__)

def main(context):
    
    


    titles = [p.title() for p in context.pages]
    while 'UniSat Wallet' not in titles:
        titles = [p.title() for p in context.pages]

    uni_page = context.pages[1]
    uni_page.wait_for_load_state()

    uni_page.click('text=I already have a wallet')

    asyncio.sleep(50)