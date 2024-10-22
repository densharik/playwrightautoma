from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)

def main(context):
    
    pages = context.pages
    page_extension = pages[0]
    print(pages)
    page_extension.locator("#root > div:nth-child(1) > div > div > div > div:nth-child(2) > div:nth-child(3)").wait_for(state="visible").click()