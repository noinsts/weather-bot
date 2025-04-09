import os
import json

from src.utils.logger import setup_logger

class WeatherTranslator:
    def __init__(self, json_path=None):
        self.translations = {}
        self.log = setup_logger()
        self.load_translations(json_path)

    def load_translations(self, json_path=None):
        try:
            # Отримуємо шлях до директорії, де знаходиться main.py
            main_dir = os.path.dirname(os.path.abspath(__file__))
            # Отримуємо шлях до директорії src
            src_dir = os.path.dirname(main_dir)
            # Формуємо шлях до weather_descriptions.json
            absolute_path = os.path.join(src_dir, 'config', 'weather_descriptions.json')

            with open(absolute_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            self.log.info(f"Переклади завантажено: {self.translations}")  # Додано для налагодження
        except FileNotFoundError:
            self.log.warning("Файл weather_descriptions.json не знайдено.")
        except json.JSONDecodeError:
            self.log.warning("Помилка декодування JSON у файлі weather_descriptions.json.")
        except Exception as e:
            self.log.warning(f"Виникла помилка: {e}")

    def translate(self, english_description):
        """Перекладає опис погоди з англійської на українську."""
        return self.translations.get(english_description.lower())
