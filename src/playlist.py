import datetime
import re

from googleapiclient.errors import HttpError

from src.channel import Youtube


class PlayList(Youtube):
    """Класс для хранения видео из плейлиста, для определения общей длительности всех видео из плейлиста и
    для вывода самого популярного видео из плейлиста по количеству лайков"""
    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста из ютуб-хостинга. Дальше все данные будут подтягиваться по API."""
        self.__playlist_id = playlist_id
        self.__videos_from_playlist = {}
        self.__title = ''
        try:
            title_playlist = self.get_service().playlists().list(id=self.__playlist_id,
                                                                 part='snippet',
                                                                 ).execute()
            if title_playlist['items']:
                self.__title = title_playlist['items'][0]['snippet']['title']
            data_playlist = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50).execute()

            if data_playlist['items']:
                for elem in data_playlist['items']:
                    id_video = elem['contentDetails']['videoId']
                    duration_video = ''
                    data_video = self.get_service().videos().list(part='snippet, statistics,'
                                                                       'contentDetails, topicDetails',
                                                                  id=id_video).execute()
                    if data_video['items']:
                        duration_video = data_video['items'][0]['contentDetails']['duration']
                    self.__videos_from_playlist[id_video] = duration_video
        except HttpError:
            self.__playlist_id = None
            self.__videos_from_playlist = {}

    def __total_duration(self) -> datetime.timedelta:
        """Метод для определения общей длительности всех видео из плейлиста"""
        sum_duration = datetime.timedelta()
        if self.__videos_from_playlist:
            for item in self.__videos_from_playlist.values():
                result = []
                second_pattern = r'(\d+)S'
                minute_pattern = r'(\d+)M'
                hour_pattern = r'(\d+)H'
                days_pattern = r'(\d+)D'
                second = re.findall(second_pattern, item)
                minute = re.findall(minute_pattern, item)
                hour = re.findall(hour_pattern, item)
                days = re.findall(days_pattern, item)
                duration = [days, hour, minute, second]
                for elem in duration:
                    if elem:
                        result.append(int(elem[0]))
                    else:
                        result.append(0)
                time_delta = datetime.timedelta(days=result[0], hours=result[1], minutes=result[2], seconds=result[3])
                sum_duration += time_delta
        return sum_duration

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает объект класса 'datetime.timedelta' с суммарной длительность плейлиста"""
        return self.__total_duration()

    @property
    def url(self) -> str:
        """Возвращает ссылку в виде строки на плейлист в YouTube"""
        return 'https://www.youtube.com/playlist?list=' + f'{self.__playlist_id}'

    @property
    def title(self) -> str:
        """Возвращает название плейлиста в виде строки"""
        return self.__title

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео по количеству лайков из текущего плейлиста """
        url_best_video = 'https://youtu.be/'
        max_likes = 0
        id_max_video = ''
        if self.__videos_from_playlist:
            for item in self.__videos_from_playlist:
                data = self.get_service().videos().list(part='statistics',
                                                        id=item).execute()
                if data['items']:
                    if int(data['items'][0]['statistics']['likeCount']) > max_likes:
                        max_likes = int(data['items'][0]['statistics']['likeCount'])
                        id_max_video = item
            url_best_video = url_best_video + id_max_video
        return url_best_video

    def __repr__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса"""
        return f"{self.__class__.__name__}('{self.__playlist_id}')"

    def __str__(self):
        """Возвращает строку с названием класса и полями при инизиализации экземпляров класса в дружественном формате"""
        result = f'Название плейлиста = {self.title}\nСсылка на плейлист = {self.url}'
        return result
