import re

def split_proxy_string(proxy_str):
    """
    Функция для разбора строки прокси на отдельные компоненты.
    """
    parts = []

    # Удаляем 'http://' или 'https://' если они есть
    if '://' in proxy_str:
        protocol, rest = proxy_str.split('://', 1)
        rest = rest.strip('/')
    else:
        rest = proxy_str

    # Разбиваем оставшуюся строку по '@'
    segments = rest.split('@')

    # Список для хранения всех частей
    all_parts = []

    for segment in segments:
        # Разбиваем каждый сегмент по ':'
        subparts = segment.split(':')
        all_parts.extend(subparts)

    # Удаляем пустые строки и пробелы
    parts = [s.strip() for s in all_parts if s.strip()]

    return parts

def parse_proxy_line(line):
    """
    Функция для парсинга одной строки прокси.
    """
    parts = split_proxy_string(line)

    proxy_data = {
        'ip': None,
        'port': None,
        'user': None,
        'password': None
    }

    # Шаблон для IP-адреса
    ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'

    # Проходим по всем частям и пытаемся определить IP и порт
    for i, part in enumerate(parts):
        if re.match(ip_pattern, part):
            # Проверяем корректность каждого октета IP-адреса
            if all(0 <= int(num) <= 255 for num in part.split('.')):
                proxy_data['ip'] = part
                # Предполагаем, что следующий элемент — порт
                if i + 1 < len(parts) and parts[i + 1].isdigit():
                    proxy_data['port'] = parts[i + 1]
                break

    # Собираем оставшиеся части для user и password
    remaining_parts = [p for p in parts if p != proxy_data['ip'] and p != proxy_data['port']]

    if len(remaining_parts) >= 2:
        proxy_data['user'] = remaining_parts[0]
        proxy_data['password'] = remaining_parts[1]
    elif len(remaining_parts) == 1:
        proxy_data['user'] = remaining_parts[0]
        proxy_data['password'] = ''
    else:
        proxy_data['user'] = ''
        proxy_data['password'] = ''

    return proxy_data

def process_proxies(input_file, output_file, output_format, format_type):
    processed_proxies = []

    # Читаем входной файл
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return 0

    for line in lines:
        line = line.strip()
        if not line or not any(x in line for x in [':', '@']):
            continue

        proxy_data = parse_proxy_line(line)

        # Проверяем, что нашли IP и порт
        if proxy_data['ip'] and proxy_data['port']:
            # Переставляем user и password, если выбран формат 2
            if format_type == '2':
                proxy_data['user'], proxy_data['password'] = proxy_data['password'], proxy_data['user']

            # Форматируем строку согласно указанному формату
            try:
                formatted = output_format.format(
                    ip=proxy_data['ip'],
                    port=proxy_data['port'],
                    user=proxy_data['user'],
                    password=proxy_data['password']
                )
                processed_proxies.append(formatted)
            except KeyError as e:
                print(f"Ошибка в формате вывода: отсутствует ключ {e}")
                return 0
        else:
            print(f"Предупреждение: Некорректная строка прокси '{line}'")

    # Записываем результат
    if processed_proxies:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(processed_proxies))
        print(f"\nОбработано и сохранено {len(processed_proxies)} прокси в файл '{output_file}'")
    else:
        print("Нет валидных прокси для сохранения.")

    return len(processed_proxies)

def main():
    print("Proxy Parser")

    input_file = input("Введите имя входного файла (по умолчанию 'proxies.txt'): ") or "proxies.txt"
    output_file = input("Введите имя выходного файла (по умолчанию 'proxies.new.txt'): ") or "proxies.new.txt"

    output_format = input("Введите формат вывода (например {ip}:{port}:{user}:{password}): ")
    if not output_format:
        output_format = "{ip}:{port}:{user}:{password}"

    # Спрашиваем формат один раз перед обработкой
    while True:
        format_type = input("Выберите формат прокси:\n1. user:pass\n2. pass:user\nВведите номер формата (1 или 2): ")
        if format_type in ['1', '2']:
            break
        print("Неверный ввод. Пожалуйста, выберите 1 или 2.")

    try:
        count = process_proxies(input_file, output_file, output_format, format_type)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
