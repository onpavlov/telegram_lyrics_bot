import configparser
from classes.telegram import Telegram

SETTINGS_PATH = 'config/settings.ini'

conf = configparser.ConfigParser()
conf.read(SETTINGS_PATH)

settings = {
    'telegram_token' : conf.get('telegram', 'telegram_token'),
    'telegram_api_link' : conf.get('telegram', 'telegram_api_link'),
    'telegram_api_host' : conf.get('telegram', 'telegram_host'),
    'musicsmatch_token': conf.get('musicsmatch', 'musicsmatch_token'),
    'musicsmatch_api_url': conf.get('musicsmatch', 'musicsmatch_api_url'),
}

telega = Telegram(settings)
telega.run()