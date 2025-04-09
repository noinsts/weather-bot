import os
import logging

def setup_logger():
    logger = logging.getLogger("aiogram_bot")
    logger.setLevel(logging.INFO)

    # Отримуємо шлях до кореня проекту (три рівні вище від поточного файлу)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 🗂️ Шлях до вкладеної папки для логів
    log_path = os.path.join(project_root, "log/debug")
    os.makedirs(log_path, exist_ok=True)

    # 📄 Формат логів
    log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 📁 Запис у log/debug/bot.log
    file_handler = logging.FileHandler(f"{log_path}/bot.log", mode="a")
    file_handler.setFormatter(log_format)

    # 🖥️ Вивід у консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # 💣 Уникаємо дублювання логів
    if logger.hasHandlers():
        logger.handlers.clear()

    # ➕ Додаємо хендлери
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
