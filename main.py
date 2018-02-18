import configparser
from classes.telegram import Telegram

SETTINGS_PATH = 'config/settings.ini';

conf = configparser.ConfigParser()
conf.read(SETTINGS_PATH)

settings = {
    'token' : conf.get('telegram', 'telegram_token'),
    'api_link' : conf.get('telegram', 'telegram_api_link'),
    'api_host' : conf.get('telegram', 'telegram_host')
}

telega = Telegram(settings)
telega.run()

# print(telega.getMe())