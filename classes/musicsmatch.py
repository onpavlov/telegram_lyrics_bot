import requests, json

class Musicsmatch:
    def __init__(self, config):
        self.LANGUAGE_CODE = 'ru'

        self.token = config['musicsmatch_token']
        self.api_link = config['musicsmatch_api_url']

    def get_top_tracks(self, country ='ru'):

        """
        Returns top 5 songs in selected country

        :param country: two-character code of country (example: ru, by, it, us...)
        :type country: str
        :return:
        """

        params = {
            'page': 1,
            'page_size': 5,
            'f_has_lyrics': 1,
            'country': country
        }
        return self.__get_body(self._get_query('chart.tracks.get', params))['track_list']

    def get_top_artists(self, country ='ru'):

        """
        Returns top 5 artists in selected country

        :param country: two-character code of country (example: ru, by, it, us...)
        :type country: str
        :return:
        """

        params = {
            'page': 1,
            'page_size': 5,
            'country': country
        }
        return self.__get_body(self._get_query('chart.artists.get', params))['artist_list']

    def get_lyrics_by_query(self, query):

        """
        Searches lyrics by query
        :param query: search query
        :type query: str
        :return:
        """

        params = {
            'f_has_lyrics': 1,
            'page': 1,
            'page_size': 1,
            's_track_rating': 'desc',
            'q': query
        }
        track_list = self.__get_body(self._get_query('track.search', params))

        if not track_list: return None

        track = track_list['track_list'].pop()
        lyrics = self.get_lyrics_by_track_id(track['track']['track_id'])

        if track and lyrics:
            return {
                'title' : track['track']['artist_name'] + ' - ' + track['track']['track_name'],
                'lyrics' : lyrics['lyrics']['lyrics_body'] + '\n\n' + lyrics['lyrics']['lyrics_copyright']
            }

        return None

    def get_translate_by_query(self, query):

        """
        Searches lyrics translate by query
        :param query: search query
        :type query: str
        :return:
        """

        params = {
            'f_has_lyrics': 1,
            'page': 1,
            'page_size': 1,
            's_track_rating': 'desc',
            'q': query
        }
        track_list = self.__get_body(self._get_query('track.search', params))

        if not track_list: return None

        track = track_list['track_list'].pop()
        lyrics = self.get_translate_by_track_id(track['track']['track_id'])

        if track and lyrics:
            return {
                'title' : track['track']['artist_name'] + ' - ' + track['track']['track_name'],
                'lyrics' : lyrics['lyrics']['lyrics_body'] + '\n\n' + lyrics['lyrics']['lyrics_copyright']
            }

        return None

    def get_lyrics_by_track_id(self, track_id):

        """
        Returns lyrics by track_id

        :param track_id: music track id
        :type track_id: int
        :return:
        """

        return self.__get_body(self._get_query('track.lyrics.get', {'track_id' : track_id}))

    def get_translate_by_track_id(self, track_id):

        """
        Returns lyrics translate to russian by track_id

        :param track_id: music track id
        :type track_id: int
        :return:
        """
        params = {'selected_language' : self.LANGUAGE_CODE,'track_id' : track_id}
        return self.__get_body(self._get_query('track.lyrics.translation.get', params))

    def _get_query(self, method ='', params = {}):

        """
        Send POST query to API

        :param method: API method
        :type method: str
        :param params: additional params
        :type params: dict
        :return:
        """

        params.update({'apikey' : self.token})
        r = requests.get(self.api_link + method, params)
        return json.loads(r.text)

    def __get_body(self, response):

        """
        :param response: dictionary response from API
        :type response: dict
        :return:
        """

        if response.get('message') and int(response['message']['header']['status_code']) == 200:
            return response['message']['body']

        return None