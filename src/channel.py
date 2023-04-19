import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_DATA_V3_API_KEY')
    currency_json_file = 'currency_json_file.json'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not isinstance(channel_id, str):
            raise ValueError('chanel_id should be string')
        self.__channel_id = channel_id
        data = self.__class__.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        if data.get("items"):
            for elem in data['items']:
                if elem.get('snippet'):
                    self.title = elem['snippet']['title']
                    self.description = elem['snippet']['description']
                    self.custom_url = elem['snippet']['customUrl']
                if elem.get('statistics'):
                    self.subscribers = elem['statistics']['viewCount']
                    self.videos = elem['statistics']['subscriberCount']
                    self.video_count = elem['statistics']['videoCount']
                else:
                    self.title = self.description = self.custom_url = None
                    self.subscribers = self.videos = self.video_count = None

    @property
    def url(self):
        return 'https://www.youtube.com/channel/' + self.__channel_id

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.YOUTUBE_API_KEY)
        return service

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.__class__.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, ensure_ascii=False, indent=2))

    def to_json(self):
        file = self.__class__.currency_json_file
        with open(file, "a") as f:
            if os.stat(file).st_size == 0:
                json.dump([self.__dict__], f)
            else:
                with open(file) as json_file:
                    data_list = json.load(json_file)
                    data_list.append(self.__dict__)
                with open(file, "w") as json_file:
                    json.dump(data_list, json_file)

