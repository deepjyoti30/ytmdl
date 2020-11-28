"""Handle inserting metadata manually."""

from datetime import datetime
from simber import Logger
from re import sub, match


logger = Logger("manual")


class Meta:
    """
    Meta Class will have properties same as
    those of Gaana and Itunes in order to make
    them compatible with the other modules
    that are using this data to write to the
    song files.

    Following properties will only be present

    release_date        : Date of Release of the song
    track_name          : Name of the song
    artist_name         : Name of the artist(s)
    collection_name     : Name of the album
    primary_genre_name  : Genre of the song
    track_number        : Number of the track in the album
    artwork_url_100     : URL of the album cover
    """
    def __init__(self):
        self.release_date = "{}T00:00:00Z".format(datetime.now().date())
        self.track_name = "N/A"
        self.artist_name = "N/A"
        self.collection_name = "N/A"
        self.primary_genre_name = "N/A"
        self.track_number = "1"
        self.artwork_url_100 = ""

    def _read_individual(self, default_value):
        """
        Read each value and do the usual checks.

        One value is confirmed legit, return it.
        """
        temp_value = input("")
        # Remove starting and terminating spaces
        # and more than one space
        temp_value = sub(r'^\ |\ $', '', temp_value)
        temp_value = sub(r'[\ ]{2,}', ' ', temp_value)

        return temp_value if temp_value != "" else default_value

    def read_values(self):
        """
        Read the values from the user and update them.
        """
        logger.info("Entering interactive mode. Press enter to skip and keep default values.")
        print("Enter date of release of the song (default: {})".format(
                    self.release_date
            ), end=": ")
        self.release_date = self._read_individual(self.release_date)

        print("Enter name of the song (default: {})".format(
                    self.track_name
            ), end=": ")
        self.track_name = self._read_individual(self.track_name)

        print("Enter name of the artist(s) (default: {})".format(
                    self.artist_name
            ), end=": ")
        self.artist_name = self._read_individual(self.artist_name)
        print("Enter name of the album (default: {})".format(
                    self.collection_name
            ), end=": ")
        self.collection_name = self._read_individual(self.collection_name)

        print("Enter genre of the song (default: {})".format(
                    self.primary_genre_name
            ), end=": ")
        self.primary_genre_name = self._read_individual(self.primary_genre_name)

        print("Enter track number (default: {})".format(
                    self.track_number
            ), end=": ")
        self.track_number = self._read_individual(self.track_number)

        print("Enter URL for album cover (default: {})".format(
                    self.artwork_url_100
            ), end=": ")
        self.artwork_url_100 = self._read_individual(self.artwork_url_100)

        logger.info("Leaving interactive mode.")


def get_data(query_name):
    """
    Get the data from the user.
    """
    meta = Meta()
    meta.track_name = query_name
    meta.read_values()
    return [meta]


if __name__ == "__main__":
    meta = Meta()
    meta.read_values()

    print(meta.release_date)
    print(meta.track_name)
    print(meta.collection_name)
    print(meta.artist_name)
    print(meta.primary_genre_name)
    print(meta.track_number)
    print(meta.artwork_url_100)
