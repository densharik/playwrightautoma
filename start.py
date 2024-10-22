import subprocess
import importlib
import os
import sys
import logging
import random
import utils.data_manager as data_manager

from logging.handlers import RotatingFileHandler
from utils.extension_manager import create_temp_extension, remove_temp_extension

from playwright.sync_api import sync_playwright

EXTENSIONS = {
    "1": {"name": "MetaMask", "path": "C:/Users/danil/Desktop/playwright/metamask"},
    "2": {"name": "UniSat", "path": "C:/Users/danil/Desktop/playwright/unisat"}
}

# Настройка логгера (без изменений)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler('script_log.log', maxBytes=5*1024*1024, backupCount=2)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


folder_path = os.path.join(os.path.dirname(__file__), 'modules')
if folder_path not in sys.path:
    sys.path.append(folder_path)

def run_cmd():
    current_script = os.path.abspath(__file__)
    cmd = f'python "{current_script}" --run_tasks'
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def main(page=None):
    run_cmd()

def run_task_in_browser(task_module, browser_type, extension_path):
    logger.info(f"Запуск браузера для модуля {task_module.__name__}")
    
    temp_extension_path = create_temp_extension(extension_path)
    try:
        proxies = data_manager.get_proxies()
        proxy = random.choice(proxies) if proxies else None
        
        extension_args = [
            f"--disable-extensions-except={temp_extension_path}",
            f"--load-extension={temp_extension_path}",
            "--no-sandbox"
        ]

        browser_options = {
            "user_data_dir": "./user_data",
            "headless": False,
            "args": extension_args
        }
        # Добавление прокси в опции браузера, если он указан
        if proxy:
            browser_options["proxy"] = proxy

        # Запуск браузера с использованием всех указанных опций
        context = browser_type.launch_persistent_context(**browser_options)
        
        logger.info("Новая страница открыта")
        logger.info(f"Браузер запущен с установленным расширением и прокси: {proxy['server'] if proxy else 'без прокси'}")
        logger.info("Новая страница открыта")
        task_module.main(context=context)
        logger.info("Выполнение main завершено")
        # Ожидание ввода пользователя перед закрытием браузера
        input("Нажмите Enter для закрытия браузера...")
    except Exception as e:
        logger.error(f"Ошибка в run_task_in_browser: {str(e)}")
        raise
    finally:
        logger.info("Закрытие браузера")
        remove_temp_extension(temp_extension_path)
        browser.close()

def run_tasks():
    print("Выберите расширение для установки:")
    for key, value in EXTENSIONS.items():
        print(f"{key}. {value['name']}")
    choice_extension = input("Введите номер расширения (1 или 2): ")

    if choice_extension in EXTENSIONS:
        extension = EXTENSIONS[choice_extension]
        logger.info(f"Выбрано расширение: {extension['name']}")
        extension_path = extension['path']
        
    else:
        logger.error("Неверный выбор. Попробуйте снова.")


    unisat_tasks = {
        "1": "unisat"
    }
    metamask_tasks = {
        "1": "metamask"
    }
    print("Выберите таск для выполнения:")
    if choice_extension == "1":
        tasks = metamask_tasks
    else:
        tasks = unisat_tasks
    for key, value in tasks.items():
        print(f"{key}. {value}")
    
    choice = input("Введите номер таска для запуска: ")
    
    if choice in tasks:
        task_name = tasks[choice]
        logger.info(f"Выбран таск: {task_name}")
        try:
            task_module = importlib.import_module(task_name)
            if not hasattr(task_module, 'main'):
                logger.error(f'У модуля {task_name} отсутствует функция main().')
            
            with sync_playwright() as p:
                run_task_in_browser(task_module, p.chromium, extension_path)
                logger.info(f"Браузер запущен с расширением {extension['name']}")

        except ImportError:
            logger.error(f"Не удалось найти модуль {task_name}")
        except AttributeError as e:
            logger.error(f"Ошибка в модуле {task_name}: {str(e)}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {str(e)}")
    else:
        logger.error("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    if "--run_tasks" in sys.argv:
        run_tasks()
        logger.info("\nЗадачи выполнены. Нажмите Enter для выхода...")
        input()
    else:
        main()

