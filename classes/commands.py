class Commands:
    def __init__(self, telegram):
        self.telegram = telegram

    def onStart(self, message):

        """
        Handler for /start command

        :param message:
        :return:
        """

        message_from = message['from']
        user_first_name = message_from['first_name']
        user_last_name = ' ' + message_from['last_name'] if (message_from.get('last_name') != None) else ''
        text = 'Привет, ' + user_first_name + user_last_name + '!\n' \
            + 'Я Lyrics bot и я помогу тебе найти текст твоей любимой песни.\n' \
            + 'Просто набери /help и посмотри что я умею!'

        self.telegram.sendMessage(text)

    def onHelp(self, *args):

        """
        Handler for /help command

        :param args:
        :return:
        """

        text = 'Вот список поддерживаемых команд:\n' \
               + '/search <Название песни>\n' \
               + '/search <Название песни>\n'

        self.telegram.sendMessage(text)

    def onSearch(self, *args):

        """
        Handler for /search command

        :param args:
        :return:
        """

        text = 'Название песни:\n' \
               + 'текст песни\n' \
               + 'текст песни\n'

        self.telegram.sendMessage(text)

    def onUnknownCommand(self, *args):

        """
        Handler for unknown command

        :param args:
        :return:
        """

        text = 'Неподдерживаемая команда. /help вам поможет :)'

        self.telegram.sendMessage(text)