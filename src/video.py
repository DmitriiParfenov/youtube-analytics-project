from src.channel import Youtube


class Video(Youtube):
    """Класс для хранения информации о видео с ютуб-хостинга"""

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео из ютуб-хостинга. Дальше все данные будут подтягиваться по API."""
        if not isinstance(video_id, str):
            raise ValueError('video_id should be string')
        self.__video_id = video_id
        data = self.get_service().videos().list(part='snippet, statistics, contentDetails, topicDetails',
                                                id=self.__video_id).execute()
        if data['items']:
            for elem in data['items']:
                if elem.get('snippet'):
                    self.title = elem['snippet']['title']
                if elem.get('statistics'):
                    self.viewCount = elem['statistics']['viewCount']
                    self.likeCount = elem['statistics']['likeCount']
                else:
                    self.title = self.viewCount = self.likeCount = None

    @property
    def url_video(self):
        """Метод возвращает ссылку на рассматриваемое видео"""
        return 'https://www.youtube.com/watch?v=' + f'{self.__video_id}'

    @property
    def id_video(self):
        return self.__video_id

    def __str__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса в дружественном формате"""
        result = ''
        for elem in self.__dict__:
            if elem == '_Video__video_id':
                result += f'Ссылка на видео = {self.url_video}\n'
            else:
                result += f'{elem} = {self.__dict__[elem]}\n'
        return result

    def __repr__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса"""
        return f"{self.__class__.__name__}('{self.__video_id}')"


class PLVideo(Video):
    """Класс для хранения идентификаторов видео и плэйлиста с ютуб-хостинга"""
    list_videos_from_playlist = []

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id плэйлиста из ютуб-хостинга. Остальные данные подтагиваются из родительского
        класса."""
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def __repr__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса"""
        return super().__repr__()[:-1] + f", '{self.__playlist_id}')"

    def __str__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса в дружественном формате"""
        res = ''
        attrs = super().__str__().split('\n')
        for obj in attrs:
            if obj.startswith('_PLVideo__playlist_id'):
                res += f'Ссылка на плэйлист = {self.url_playlist}\n'
            else:
                res += f'{obj}\n'
        return res

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def url_playlist(self):
        return 'https://WWW.YouTube.Com/playlist?list=' + f'{self.__playlist_id}'

    @classmethod
    def get_videos_from_playlist_id(cls, playlist_id):
        """Класс-метод из заданного плэйлиста добавляет в атрибут класса PLVideo все id видео из плэйлиста.
        Далее происходит создание экземпляров родительского класса по полученным id."""
        data = cls.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                      maxResults=50).execute()
        if data['items']:
            for item in data['items']:
                if item.get('contentDetails'):
                    cls.list_videos_from_playlist.append(cls.__bases__[0](item['contentDetails']['videoId']))
