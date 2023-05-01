import json
import os

from googleapiclient.discovery import build


class Youtube:
    """Класс-миксин для хранения API-ключа и вызова метода для работы с youtube API."""
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_DATA_V3_API_KEY')

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        service = build('youtube', 'v3', developerKey=cls.YOUTUBE_API_KEY)
        return service


class Channel(Youtube):
    """Класс для ютуб-канала"""
    currency_json_file = 'currency_json_file.json'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not isinstance(channel_id, str):
            raise ValueError('chanel_id should be string')
        self.__channel_id = channel_id
        data = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        if data.get("items"):
            for elem in data['items']:
                if elem.get('snippet'):
                    self.title = elem['snippet']['title']
                    self.description = elem['snippet']['description']
                    self.custom_url = elem['snippet']['customUrl']
                if elem.get('statistics'):
                    self.view_count = elem['statistics']['viewCount']
                    self.subscribers = elem['statistics']['subscriberCount']
                    self.video_count = elem['statistics']['videoCount']
                else:
                    self.title = self.description = self.custom_url = None
                    self.subscribers = self.videos = self.video_count = None

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Метод возвращает сумму количества подписчиков"""
        if not self.subscribers.isdigit():
            raise ValueError('Количество подписчиков должно быть числом')
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        """Метод возвращает разность количества подписчиков"""
        if not self.subscribers.isdigit():
            raise ValueError('Количество подписчиков должно быть числом')
        return int(self.subscribers) - int(other.subscribers)

    def __gt__(self, other):
        """Метод возвращает True, если количество подписчиков в 'other' меньше чем в текущем экземпляре,
        иначе — False"""
        if not self.subscribers.isdigit():
            raise ValueError('Количество подписчиков должно быть числом')
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        """Метод возвращает True, если количество подписчиков в 'other' меньше или равно чем в текущем экземпляре,
        иначе — False"""
        if not self.subscribers.isdigit():
            raise ValueError('Количество подписчиков должно быть числом')
        return int(self.subscribers) >= int(other.subscribers)

    def __eq__(self, other):
        """Метод возвращает True, если количество подписчиков в 'other' равно количеству подписчиков в текущем
        экземпляре, иначе — False"""
        if not self.subscribers.isdigit():
            raise ValueError('Количество подписчиков должно быть числом')
        return int(self.subscribers) == int(other.subscribers)

    @property
    def url(self):
        return 'https://www.youtube.com/channel/' + self.__channel_id

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, ensure_ascii=False, indent=2))

    def to_json(self):
        file = self.currency_json_file
        with open(file, "a") as f:
            if os.stat(file).st_size == 0:
                json.dump([self.__dict__], f)
            else:
                with open(file) as json_file:
                    data_list = json.load(json_file)
                    data_list.append(self.__dict__)
                with open(file, "w") as json_file:
                    json.dump(data_list, json_file)

