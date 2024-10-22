import os
import shutil
import tempfile

def create_temp_extension(original_path):
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    
    # Копируем содержимое оригинального расширения во временную директорию
    temp_extension_path = os.path.join(temp_dir, 'extension')
    shutil.copytree(original_path, temp_extension_path)
    
    return temp_extension_path

def remove_temp_extension(temp_path):
    # Удаляем временную директорию с расширением
    shutil.rmtree(temp_path, ignore_errors=True)