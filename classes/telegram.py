import requests, json, time
from classes.commands import Commands

class Telegram:
    def __init__(self, config):

        """
        :param config: API configuration
        :type dict
        """

        self.cmd = Commands(self)
        self.last_update_id = ''
        self.token = config['token']
        self.api_link = config['api_link']
        self.api_host = config['api_host']
        self.commands = {
            '/start' : self.cmd.onStart,
            '/help' : self.cmd.onHelp,
            '/search' : self.cmd.onSearch
        }

    def getMe(self):

        """
        :return: bot info
        """

        return self._postQuery('getMe')

    def run(self, latency = 2):

        """
        Runs request loop

        :param latency:
        :type int
        :return:
        """

        params = {}

        while(1):
            time.sleep(latency)

            if (len(str(self.last_update_id)) > 0):
                params['offset'] = self.last_update_id

            updates = self._getUpdates(params)

            if (bool(updates['ok'])):
                for update in updates['result']:
                    if (self.last_update_id == update['update_id']): continue

                    self.last_update_id = update['update_id']
                    message = update['message']

                    if self.__isCommandEntity(message):
                        self._getResponse(message)

    def _getResponse(self, message = {}):

        """
        Executes method from commands dictionary

        :param message:
        :type dict
        :return:
        """

        self.chat_id = message['chat']['id'] if (message.get('chat') != None) else 0
        command = message['text'] if (message.get('text') != None) else '/start'

        if (self.commands.get(command) != None):
            self.commands[command](message)
        else:
            self.cmd.onUnknownCommand()

    def sendMessage(self, text = ''):
        params = {
            'chat_id' : self.chat_id,
            'text' : text
        }

        self._postQuery('sendMessage', params)

    def _getUpdates(self, params = {}):

        """
        Returns list of updates

        :param params:
        :return:
        """

        return self._postQuery('getUpdates', params)

    def _postQuery(self, method = '', params = {}):

        """
        Send POST query to API

        :param method:
        :param params:
        :return:
        """

        query = self.api_link + 'bot' + self.token + '/' + method
        r = requests.post(query, params)
        return json.loads(r.text)

    def __isCommandEntity(self, message):

        """
        Checks type of entity

        :param message:
        :return:
        """

        entities = message.get('entities')

        if entities != None:
            if entities.pop()['type'] == 'bot_command':
               return True

        return False