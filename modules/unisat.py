from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext
import os
import logging

logger = logging.getLogger(__name__)

def get_all_titles(context):
    """
    Безопасно получает заголовки всех страниц
    """
    titles = []
    for page in context.pages:
        try:
            # Проверяем, что страница не закрыта
            if not page.is_closed():
                # Ждем немного загрузки страницы
                page.wait_for_load_state('domcontentloaded', timeout=1000)
                title = page.title()
                titles.append(title)
        except Exception as e:
            logger.debug(f"Не удалось получить заголовок страницы: {str(e)}")
            continue
    return titles

def main(context):
    password = "password"
    seed_phrase = os.getenv('UNISAT_TEST_PHRASE')


    titles = [p.title() for p in context.pages]
    while 'UniSat Wallet' not in titles:
        titles = [p.title() for p in context.pages]
    mint_page = context.new_page()
    uni_page = context.pages[1]
    uni_page.wait_for_load_state('networkidle')  # Ждем полной загрузки страницы
    
    if uni_page.is_visible('text=I already have a wallet'):
        uni_page.click('text=I already have a wallet')
        uni_page.wait_for_timeout(1000)  # Пауза 1 секунда после клика

    if uni_page.is_visible('input[type="password"]'):
        uni_page.fill('input[type="password"]', password)
        logger.info("Введен пароль в поле ввода пароля")
        uni_page.wait_for_timeout(500)

    if uni_page.is_visible('input[placeholder="Confirm Password"]'):
        uni_page.fill('input[placeholder="Confirm Password"]', password)
        logger.info("Введен пароль в поле подтверждения пароля")

    if uni_page.is_visible('text=Continue'):
        uni_page.click('text=Continue')
        uni_page.wait_for_timeout(1500)  # Пауза 1.5 секунды после финального клика
    if uni_page.is_visible('text=UniSat Wallet'):
        logger.info("найдена кнопка UniSat Wallet")
        uni_page.click('text=UniSat Wallet')
        uni_page.wait_for_timeout(1500)
    # metamask.py (примерно где была проверка is_visible)
    if uni_page.is_visible("input[type='password']"):
        # Сначала копируем seed_phrase в буфер обмена
        uni_page.evaluate(f"navigator.clipboard.writeText('{seed_phrase}')")
        # Кликаем на первое поле для фокуса
        uni_page.click("input[type='password']")
        # Имитируем нажатие Ctrl+V
        uni_page.keyboard.press("Control+V")
        uni_page.wait_for_timeout(1500)
    if uni_page.is_visible('text=Continue'):
        uni_page.click('text=Continue')
        uni_page.wait_for_timeout(1500)
    if uni_page.is_visible('text=Taproot'):
        uni_page.click('text=Taproot')
        uni_page.wait_for_timeout(1500)
    if uni_page.is_visible('text=Continue'):
        uni_page.click('text=Continue')
        uni_page.wait_for_timeout(1500)
    if uni_page.is_visible('input[type="checkbox"]'):
        uni_page.wait_for_timeout(3000)
        uni_page.locator('input[type="checkbox"]').nth(0).check()  # первый
        uni_page.wait_for_timeout(100)
        uni_page.locator('input[type="checkbox"]').nth(1).check()  # второй
        uni_page.wait_for_timeout(100)
        uni_page.click('text=OK')

    if uni_page.is_visible('input[type="password"]'):
        uni_page.fill('input[type="password"]', password)
        logger.info("Введен пароль в поле ввода пароля")
        uni_page.wait_for_timeout(500)
    if uni_page.is_visible('text=Unlock'):
        uni_page.click('text=Unlock')
    
    mint_page.goto('https://fractal.unisat.io/runes/inscribe')
    mint_page.wait_for_load_state('networkidle')
    mint_page.click('text=Connect')
    mint_page.wait_for_timeout(100)
    mint_page.click('text=UniSat Wallet')
    mint_page.wait_for_timeout(1500)
    titles = get_all_titles(context)
    popup = context.pages[3]
    if popup.wait_for_selector('xpath=//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div', state='visible', timeout=5000):
        logger.info("Кнопка Connect видна.")
        popup.locator('xpath=//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div').click()
    titles = get_all_titles(context)
    popup = context.pages[-1]
    if popup.wait_for_selector('xpath=//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div', state='visible', timeout=5000):
        popup.locator('xpath=//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div').click()
    titles = get_all_titles(context)
    popup = context.pages[-1]
    if popup.wait_for_selector('xpath=//*[@id="root"]/div[1]/div/div[2]/div/div[2]/div', state='visible', timeout=5000):
        popup.locator('xpath=//*[@id="root"]/div[1]/div/div[2]/div/div[2]/div').click()
        
