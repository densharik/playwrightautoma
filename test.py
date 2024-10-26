from playwright.sync_api import sync_playwright
import logging
import random
import time

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserAutomation:
    """
    Класс для автоматизации действий в браузере
    """
    def __init__(self, headless=False):
        """
        Конструктор класса - выполняется при создании объекта
        :param headless: Запускать ли браузер в фоновом режиме
        """
        self.headless = headless
        self.browser = None
        self.page = None
        
    def start_browser(self):
        """Запуск браузера и создание новой страницы"""
        # Запускаем драйвер браузера
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=['--start-maximized']
        )
        # Создаем новую страницу
        self.page = self.browser.new_page(viewport={'width': 1920, 'height': 1080})
        logger.info("🚀 Браузер успешно запущен")
        
    def open_website(self, url: str):
        """
        Открытие указанного сайта
        :param url: адрес сайта для открытия
        """
        try:
            self.page.goto(url)
            self.page.wait_for_load_state('networkidle')
            logger.info(f"✨ Открыт сайт: {url}")
        except Exception as e:
            logger.error(f"❌ Ошибка при открытии сайта: {e}")
            
    def search_google(self, query: str):
        """
        Поиск в Google
        :param query: поисковый запрос
        """
        try:
            # Ждем загрузки поля поиска и вводим запрос
            search_box = self.page.locator('textarea[name="q"]')
            search_box.fill(query)
            search_box.press('Enter')
            
            # Ждем результаты поиска
            self.page.wait_for_selector('div#search')
            logger.info(f"🔍 Выполнен поиск по запросу: {query}")
            
            # Немного ждем, чтобы увидеть результаты
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Ошибка при поиске: {e}")
    
    def get_random_link(self):
        """Клик по случайной ссылке из результатов поиска"""
        try:
            # Получаем все ссылки из результатов поиска
            links = self.page.locator('div#search a')
            count = links.count()
            
            if count > 0:
                # Выбираем случайную ссылку из первых 5 результатов
                random_index = random.randint(0, min(5, count-1))
                random_link = links.nth(random_index)
                
                # Получаем текст ссылки для лога
                link_text = random_link.inner_text()
                logger.info(f"🎲 Выбрана случайная ссылка: {link_text}")
                
                # Кликаем по ссылке
                random_link.click()
                self.page.wait_for_load_state('networkidle')
                time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Ошибка при клике по ссылке: {e}")
    
    def close_browser(self):
        """Закрытие браузера"""
        if self.browser:
            self.browser.close()
            logger.info("👋 Браузер закрыт")

def main():
    """
    Основная функция для демонстрации работы класса
    """
    # Создаем объект нашего класса
    # Параметр headless=False означает, что браузер будет видимым
    bot = BrowserAutomation(headless=False)
    
    try:
        # Запускаем браузер
        bot.start_browser()
        
        # Открываем Google
        bot.open_website("https://www.google.com")
        
        # Выполняем поиск
        bot.search_google("Python automation tutorial")
        
        # Кликаем по случайной ссылке
        bot.get_random_link()
        
        # Ждем 5 секунд перед закрытием
        time.sleep(5)
        
    except Exception as e:
        logger.error(f"❌ Произошла ошибка: {e}")
        
    finally:
        # Закрываем браузер в любом случае
        bot.close_browser()

if __name__ == "__main__":
    main()


