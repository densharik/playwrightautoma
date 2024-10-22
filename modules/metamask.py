from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)

def main(browser):
    page = browser.new_page()
    page.goto("chrome://extensions/")

    toggle_dev = page.locator("#devMode")
    toggle_dev.wait_for(state="visible")
    
    if toggle_dev.get_attribute("aria-pressed") != "true":
        toggle_dev.click()

    page.wait_for_timeout(300)
    id_metamask = page.locator("#extension-id")
    id_metamask.wait_for(state="visible")
    extension_id = id_metamask.inner_text().split(":")[1].strip()
    metamask = page.context.new_page()
    metamask.goto(f"chrome-extension://{extension_id}/home.html#onboarding/welcome")
    
    # Здесь нужно добавить логику для дальнейших действий
    # Например, ожидание определенного элемента или выполнение других операций
    metamask.wait_for_selector("body")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        main(page)
        browser.close()