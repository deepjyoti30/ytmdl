"""Store all the exceptions related to ytmdl that might
arise during the runtime of the app
"""


class DownloadError(Exception):
    """Exception for download error.

    This exception is solely for those cases when
    the download fails for some reason.
    """
    def __init__(self, link, error) -> None:
        super().__init__()

        self.__message = self.__build_message(link, error)

    def __build_message(self, link, error) -> str:
        """Build the error message."""
        return "Download failed for `{}` with error: {}".format(
            link, error
        )

    def __str__(self) -> str:
        return self.__message


class ConvertError(Exception):
    """Exception for conversion erros.

    This exception is raised whenever the conversion goes wrong,
    mostly while using ffmpeg or something similar.
    """
    def __init__(self, error) -> None:
        super().__init__()

        self.__message = self.__build_message(error)

    def __build_message(self, error) -> str:
        """Build the error message"""
        return "Conversion failed with error: {}".format(error)

    def __str__(self) -> str:
        return self.__message


class NoMetaError(Exception):
    """Exception to be raised when no metadata is found."""
    def __init__(self, song) -> None:
        super().__init__()

        self.__message = self.__build_message(song)

    def __build_message(self, song) -> str:
        """Build the error message"""
        return "No metadata found for `{}`".format(song)

    def __str__(self) -> str:
        return self.__message


class MetadataError(Exception):
    """Exception for metadata related errors while setting metadata

    This is only to be raised when something goes wrong while setting
    the metadata for the song.
    """
    def __init__(self, song) -> None:
        super().__init__()

        self.__message = self.__build_message(song)

    def __build_message(self, song) -> str:
        """Build the error message"""
        return "Something went wrong while setting metadata for `{}`".format(
            song
        )

    def __str__(self) -> str:
        return self.__message


class ExtractError(Exception):
    """
    Exception for errors that arise while extracting any detail
    related to the song.

    This is only to be raise when some extraction related error
    occurs.
    """
    def __init__(self, song) -> None:
        super().__init__()

        self.__message = self.__build_message(song)

    def __build_message(self, song) -> str:
        return "Couldn't extract data for: {}".format(song)

    def __str__(self) -> str:
        return self.__message
