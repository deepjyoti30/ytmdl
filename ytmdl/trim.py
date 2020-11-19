"""
Handle the stuff related to trimming the song
in order to remove the speech.
"""

from inaSpeechSegmenter import Segmenter
from warnings import filterwarnings
from os import environ, remove, rename
import ffmpeg
from simber import Logger

# Setup the logger name
logger = Logger("Trimmer")


# Remove the warnings from tensorflow
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# Ignore warnings
filterwarnings("ignore")


class Trim:
    """
    Class that will handle the processing of the files.

    filename: File that we want to process.

    We will run the speech segmenter on it and get
    the music timestamps. Once we have the stamps, we can just
    trim the music part from the song and keep the name same.
    """
    def __init__(self, filename):
        self.filename = filename
        self.segmenter = Segmenter(
                                vad_engine='smn',
                                detect_gender=False,
                                ffmpeg='ffmpeg'
                            )
        self._find_music()
        self._trim()

    def _find_music(self):
        """
        Call the segmenter on the file and extract the
        music timestamps from there.
        """
        segmentation = self.segmenter(self.filename)
        logger.debug("Segmentation tuple: {}".format(segmentation))

        # Only keep all the music stamps
        segmentation = [stamp for stamp in segmentation if stamp[0] == "music"]

        if not len(segmentation):
            logger.critical(
                "Could not find music in the file. Try disabling trimming!"
            )

        # We want to consider just the last time stamp tuple,
        # Mostly there are just one time stamp with music, but sometimes
        # it can be more than one.
        segmentation = segmentation[-1]
        self.start_time = segmentation[1]
        self.end_time = segmentation[2]

        logger.debug("ST: {}\nET: {}".format(self.start_time, self.end_time))

    def _trim(self):
        """
        Use ffmpeg to trim the song to the time stamps calculated.

        Make the changes to a temp file.
        Once the work is done remove the original file and rename
        the temporary to original one.
        """
        logger.info("Trimming the song to the found time stamps")

        # Create the temp file name
        temp_name = "{}_temp.{}".format(
                                    self.filename,
                                    self.filename.split(".")[-1]
                                )

        ffmpeg.input(self.filename).output(
                                        temp_name,
                                        loglevel="panic",
                                        ss=self.start_time,
                                        to=self.end_time
                    ).run()

        # Once that's done, remove the original file
        remove(self.filename)
        # Now rename the file.
        rename(temp_name, self.filename)
        logger.info("Trimmed the file succesfully!")
