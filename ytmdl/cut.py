from .utility import exe
from . import logger
from os import remove, rename

logger = logger.Logger('cut')
LOG_FILE = logger.get_log_file()

COMMAND_CUT = 'ffmpeg -y -i "{}" -ss {} {} -c copy "{}" -loglevel error'
COMMAND_CONCAT = 'ffmpeg -y -i "concat:{}" -c copy "{}" -loglevel error'

ERROR_MESSAGE_CUT = 'There was an error while cutting, the program will continue without it. ' \
    + 'Please check "{}" for more details.'.format(LOG_FILE)
ERROR_MESSAGE_PARAMS_ASCENDING = 'Cut parameters are not in ascending order.'
ERROR_MESSAGE_PARAMS_COUNT = 'More than one parameter is passed for cut and the number is not even. ' \
    + 'Please pass a valid number of parameters.'


class CutError(Exception):
    """Represents an error while cutting the song"""
    pass


class Cut:
    """Cut song based on parameters using ffmpeg"""

    def __init__(self, path, cut_parameters):
        self.path = path
        self.cut_parameters = cut_parameters
        self._cut_song()

    def _cut_song(self):
        TEMP_PATH = "{}_temp.{}".format(
            self.path,
            self.path.split(".")[-1]
        )
        print(TEMP_PATH)
        try:
            if len(self.cut_parameters) != 1 and len(self.cut_parameters) % 2:
                logger.error(ERROR_MESSAGE_PARAMS_COUNT)
                raise CutError(ERROR_MESSAGE_PARAMS_COUNT)

            times_seconds_list = list(
                map(_get_converted_time, self.cut_parameters))
            # if we only have one parameter
            if len(times_seconds_list) == 1:
                command_formatted = COMMAND_CUT.format(
                    self.path, times_seconds_list[0], '', TEMP_PATH)
                output, error = exe(command_formatted)
                if error:
                    raise CutError(error)
                _replace_path(TEMP_PATH, self.path)

            # if we have multiple params
            elif times_seconds_list == sorted(times_seconds_list):
                time_pairs = list(_pair_generator(times_seconds_list))
                files_to_concat = []
                for index, pair in enumerate(time_pairs):
                    new_path = "{}_temp_{}.{}".format(
                        self.path,
                        index,
                        self.path.split(".")[-1]
                    )
                    to_flag = '-to {}'
                    command_formatted = COMMAND_CUT.format(
                        self.path, pair[0], to_flag.format(pair[1]), new_path)
                    output, error = exe(command_formatted)
                    if error:
                        raise CutError(error)
                    files_to_concat.append(new_path)

                command_formatted = COMMAND_CONCAT.format(
                    '|'.join(files_to_concat), TEMP_PATH)
                output, error = exe(command_formatted)
                if error:
                    raise CutError(error)
                # Remove intermediate files and old file
                for cut_path in files_to_concat:
                    remove(cut_path)
                _replace_path(TEMP_PATH, self.path)

            else:
                logger.error(ERROR_MESSAGE_PARAMS_ASCENDING)

        except Exception as e:
            logger.debug('{}'.format(e))
            logger.error(ERROR_MESSAGE_CUT)


def _pair_generator(to_split):
    """Generator for pairs of intervals"""
    for i in range(0, len(to_split), 2):
        yield to_split[i:i + 2]


def _get_converted_time(time):
    """Convert time string to seconds"""
    if time is not None:
        sec_values = [1]
        time_split = time.split(":")
        time_units = len(time_split)
        if time_units > 1:
            sec_values.insert(0, 60)
        if time_units == 3:
            sec_values.insert(0, 3600)
        return sum(x * int(t) for x, t in zip(sec_values, time.split(":")))
    return None


def _replace_path(temp, final):
    """Replaces old path with the temporary one"""
    remove(final)
    rename(temp, final)
