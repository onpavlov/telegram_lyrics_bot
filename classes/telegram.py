import requests, json, time
from classes.commands import Commands

class Telegram:
    def __init__(self, config):

        """
        :param config: API configuration
        :type config: dict
        """

        self.cmd = Commands(self, config)
        self.last_update_id = ''
        self.token = config['telegram_token']
        self.api_link = config['telegram_api_link']
        self.api_host = config['telegram_api_host']
        self.commands = self.cmd.get_commands()

    def get_me(self):

        """
        Returns dictionary with information about bot

        :return: bot info
        """

        return self._post_query('getMe')

    def run(self, latency = 2):

        """
        Runs request loop

        :param latency: latency between requests
        :type latency: int
        :return:
        """

        params = {}

        while True:
            time.sleep(latency)

            if (len(str(self.last_update_id)) > 0):
                params['offset'] = self.last_update_id

            updates = self._get_updates(params)

            if (bool(updates['ok'])):
                for update in updates['result']:
                    if (self.last_update_id == update['update_id']): continue

                    self.last_update_id = update['update_id']
                    message = update.get('message', update.get('edited_message'))

                    if self.__is_command_entity(message):
                        self._get_response(message)
            else:
                print('Error ' + str(updates['error_code']) + ': ' + updates['description'])
                break

    def _get_response(self, message = {}):

        """
        Executes method from commands dictionary

        :param message: object Message
        :type message: dict
        :return:
        """

        self.chat_id = message['chat']['id'] if message.get('chat') else 0
        command = message.get('text', '/start')
        command = command.split(' ', 1)
        params = {'query' : command[1]} if len(command) > 1 else message

        if self.commands.get(command[0]):
            self.commands[command[0]](params)
        else:
            self.cmd.on_unknown_command()

    def send_message(self, text =''):

        """
        Send message to chat

        :param text: text of message
        :type text: str
        :return:
        """

        params = {
            'chat_id' : self.chat_id,
            'text' : text,
            'parse_mode' : 'markdown'
        }

        self._post_query('sendMessage', params)

    def _get_updates(self, params = {}):

        """
        Returns list of updates

        :param params: additional query parameters
        :type params: dict
        :return:
        """

        return self._post_query('getUpdates', params)

    def _post_query(self, method ='', params = {}):

        """
        Send POST query to API

        :param method: API method
        :type method: str
        :param params: additional query params
        :type params: dict
        :return:
        """

        r = requests.post(self.api_link + 'bot' + self.token + '/' + method, params)
        return json.loads(r.text)

    def __is_command_entity(self, message):

        """
        Checks type of entity

        :param message: object Message
        :type message: dict
        :return:
        """

        entities = message.get('entities')

        if entities:
            if entities.pop()['type'] == 'bot_command':
               return True

        return False