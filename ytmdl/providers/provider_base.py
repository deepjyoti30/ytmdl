from abc import ABC, abstractmethod


class Song(ABC):
    """Abstract base class for the song. All the other song types inherit this"""
    def __init__(self, track_name, artist_name,
                 artwork_url_100, duration, provider,
                 collection_id='', track_id='', collection_name='',
                 primary_genre_name='', track_number='', release_date=''):
        self.track_name = track_name
        self.artist_name = artist_name
        self.provider = provider
        self.collection_id = collection_id
        self.track_id = track_id
        self.collection_name = collection_name
        self.artwork_url_100 = artwork_url_100
        self.primary_genre_name = primary_genre_name
        self.track_number = track_number
        self.release_date = release_date
        self.track_time = self._convert_time(duration)

    @abstractmethod
    def get_more_data(self):
        pass

    @staticmethod
    def _convert_time(duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time


class Provider(ABC):
    """Abstract base class for the provider. All the providers inherit from this"""
    def __init__(self, name='NO_NAME'):
        self._name = name

    # We make the name readonly after init
    @property
    def name(self):
        return self._name

    @abstractmethod
    def search_song(query, limit=40):
        pass


if __name__ == '__main__':
    print('This shouldn\'t be imported as a main module.')
