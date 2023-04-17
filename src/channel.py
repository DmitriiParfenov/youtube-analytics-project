import json
import os

from googleapiclient.discovery import build

# Объявление глобальных переменных
YOUTUBE_API_KEY = os.getenv('YOUTUBE_DATA_V3_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not isinstance(channel_id, str):
            raise ValueError('chanel_id should be string')
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, ensure_ascii=False, indent=2))
