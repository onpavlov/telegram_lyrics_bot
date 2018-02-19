from .musicsmatch import Musicsmatch

class Commands:
    def __init__(self, telegram, config):
        self.DEFAULT_COUNTRY_CODE = 'ru'

        self.telegram = telegram
        self.musicsmatch = Musicsmatch(config)
        self.commands = {
            '/start' : self.on_start,
            '/help' : self.on_help,
            '/search' : self.on_search,
            '/toptracks' : self.on_top_tracks,
            '/topartists' : self.on_top_artists,
            '/translate' : self.on_translate_query
        }

    def get_commands(self):

        """
        :return: dictionary available commands
        """

        return self.commands

    def on_start(self, message):

        """
        Handler for /start command

        :param message: object Message
        :type message: dict
        :return:
        """

        message_from = message['from']
        user_first_name = message_from['first_name']
        user_last_name = ' ' + message_from['last_name'] if message_from.get('last_name') else ''
        text = 'Привет, ' + user_first_name + user_last_name + '!\n' \
            + 'Я Lyrics bot и я помогу тебе найти текст твоей любимой песни.\n' \
            + 'Просто набери /help и посмотри что я умею!'

        self.telegram.send_message(text)

    def on_help(self, *args):

        """
        Handler for /help command

        :param args:
        :return:
        """

        text = 'Список поддерживаемых команд:\n' \
                + '/toptracks *<Код страны>* - выводит ТОП5 песен страны (пример: /toptracks it)\n' \
                + '/topartists *<Код страны>* - выводит ТОП5 исполнителей страны (пример: /topartists au)\n' \
                + '/search *<Название песни>* - ищет текст песни по исполнителю, названию и словам из текста\n' \
                + '/translate *<Название песни>* - ищет перевод текста песни по исполнителю, названию и словам из текста' \
                + ' _(к сожалению функция не работает на тестовом аккаунте)_\n'

        self.telegram.send_message(text)

    def on_search(self, params):

        """
        Handler for /search command

        :param params: additional params
        :type params: dict
        :return:
        """

        text = 'По вашему запросу ничего не найдено :('
        query = params.get('query')

        if query:
            response = self.musicsmatch.get_lyrics_by_query(query)

            if response:
                text = '*' + response['title'] + '*\n\n' + response['lyrics']

        self.telegram.send_message(text)

    def on_top_tracks(self, params):

        """
        Handler for /toptracks command

        :param params: additional params
        :type params: dict
        :return:
        """

        text = 'К сожалению ничего не найдено :('
        country_code = params['query'] if params.get('query') else self.DEFAULT_COUNTRY_CODE
        result = self.musicsmatch.get_top_tracks(country_code)

        if result:
            i = 1
            text = 'Топ 5 песен ' + self.__get_country_by_code(country_code) + ':\n\n'

            for song in result:
                track = song['track']
                duration = divmod(int(track['track_length']), 60)
                text += '*' + str(i) + '. ' + track['artist_name'] + '* - _' + track['track_name'] \
                        + '\n_ (Альбом: "' + track['album_name'] + '", Длительность: ' \
                        + str(duration[0]) + ':' + str(duration[1]) + ')\n\n'
                i += 1

        self.telegram.send_message(text)

    def on_top_artists(self, params):

        """
        Handler for /topartists command

        :param params: additional params
        :type params: dict
        :return:
        """

        text = 'К сожалению ничего не найдено :('
        country_code = params['query'] if params.get('query') else self.DEFAULT_COUNTRY_CODE
        result = self.musicsmatch.get_top_artists(country_code)

        if result:
            i = 1
            text = 'Топ 5 исполнителей ' + self.__get_country_by_code(country_code) + ':\n\n'

            for artist in result:
                artist = artist['artist']
                genres_list = []

                for genre in artist['primary_genres']['music_genre_list']:
                    genres_list.append(genre['music_genre']['music_genre_name'])

                text += '*' + str(i) + '. ' + artist['artist_name'] + '*' + ' _Рейтинг: ' + str(artist['artist_rating']) + '_\n' \
                        + 'Жанр: ' + str(', '.join(genres_list)) + '\n\n'
                i += 1

        self.telegram.send_message(text)

    def on_translate_query(self, params):

        """
        Handler for /translate command

        :param params: additional params
        :type params: dict
        :return:
        """

        text = 'По вашему запросу ничего не найдено :('
        query = params.get('query')

        if query:
            response = self.musicsmatch.get_translate_by_query(query)

            if response:
                text = '*' + response['title'] + '*\n\n' + response['lyrics']

        self.telegram.send_message(text)

    def on_unknown_command(self, *args):

        """
        Handler for unknown command

        :param args:
        :return:
        """

        self.telegram.send_message('Неподдерживаемая команда. /help вам поможет :)')

    def __get_country_by_code(self, country_code):

        """
        :param country_code: two-character code of country (example: ru, by, it, us...)
        :type country_code: str
        :return:
        """

        countries = {
            'ru': 'России',
            'it': 'Италии',
            'au': 'Австралии',
            'by': 'Белоруссии',
            'us': 'США',
            'kz': 'Казахстана'
        }

        return countries[country_code] if countries.get(country_code) else '(Код страны = ' + country_code + ')'