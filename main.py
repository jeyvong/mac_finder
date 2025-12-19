import json
import getpass
import logging
from modules.traceroute_mac import traceroute_mac

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mac_finder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Запуск скрипта mac_finder")

        # Загружаем конфигурацию
        logger.info("Чтение config.json")
        with open("config.json", encoding='utf-8') as f:
            cfg = json.load(f)
        logger.info(f"Конфигурация загружена: {cfg}")

        # Загружаем учетные данные
        logger.info("Чтение cred.json")
        with open("cred.json", encoding='utf-8') as f:
            cred = json.load(f)
        logger.info(f"Учетные данные загружены: {cred}")

        # Запрашиваем пароль
        logger.info(f"Запрос пароля для пользователя {cred['username']}")
        password = getpass.getpass(f"Введите пароль для пользователя {cred['username']}: ")
        logger.info("Пароль успешно введен")

        # Вызываем traceroute_mac
        logger.info(f"Запуск traceroute_mac для MAC: {cfg['target_mac']}")
        traceroute_mac(
            cfg["start_switch"],
            cred["username"],
            password,
            cfg["target_mac"].lower()
        )
        logger.info("traceroute_mac завершен")

    except FileNotFoundError as e:
        logger.error(f"Ошибка: Файл не найден - {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка: Неверный формат JSON - {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()