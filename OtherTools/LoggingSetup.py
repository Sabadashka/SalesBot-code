import logging


def setup_menu_logger():
    menu_logger = logging.getLogger('menu_clicks')
    menu_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('menu_clicks.log', encoding='utf-8')

    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    menu_logger.addHandler(file_handler)

    return menu_logger

