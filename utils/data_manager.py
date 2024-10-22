import os
import logging

logging.basicConfig(level=logging.INFO)

def read_file_to_list(file_path):
    logging.info(f"Чтение файла: {file_path}")
    if not os.path.exists(file_path):
        logging.error(f"Файл {file_path} не найден.")
        return []
    
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]
    
def parse_proxy(proxy_string):
    logging.info(f"Парсинг прокси: {proxy_string}")
    parts = proxy_string.split('@')
    if len(parts) == 2:
        ip_port, auth = parts
        protocol, ip_port = ip_port.split('://')
        ip, port = ip_port.split(':')
        username, password = auth.split(':')
        return {
            'server': f"http://{ip}:{port}",
            'username': username,
            'password': password,
        }
    
    logging.error(f"Неправильный формат прокси: {proxy_string}")
    return None

def get_seed_btc():
    logging.info("Получение BTC ")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    seed_btc_path = os.path.join(current_dir, 'seed_btc.txt')
    return read_file_to_list(seed_btc_path)

def get_seed_evm():
    logging.info("Получение EVM")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    seed_evm_path = os.path.join(current_dir, 'seed_evm.txt')
    return read_file_to_list(seed_evm_path)

def get_proxies():
    logging.info("Получение проксей")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proxies_path = os.path.join(current_dir, 'proxies.txt')
    return [parse_proxy(proxy) for proxy in read_file_to_list(proxies_path) if parse_proxy(proxy)]


if __name__ == "__main__":
    logging.info("Начало работы программы")