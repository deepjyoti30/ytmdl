import urllib.request
import sys
import time
from os import path
from os import popen
import argparse

# import traceback ## Required to debug at times.


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('URL', help="URL of the file",
                        default=None, type=str)
    parser.add_argument('des', help="The name of the file\
                        to be saved with.", default=None, nargs='?')

    args = parser.parse_args()
    return args


class Download:

    def __init__(self, URL, des=None):
        self.URL = URL
        self.des = des
        self.headers = {}
        self.f_size = 0

    def _build_headers(self, rem):
        """Build headers according to requirement."""
        self.headers = {"Range": "bytes={}-".format(rem)}
        print("Trying to resume download at: {} bytes".format(rem))

    def _preprocess_conn(self):
        """Make necessary things for the connection."""
        self.req = urllib.request.Request(url=self.URL, headers=self.headers)

        try:
            self.conn = urllib.request.urlopen(self.req)
        except Exception as e:
            print("ERROR: {}".format(e))
            exit()

        self.f_size = int(self.conn.info()['Content-Length'])

    def _get_terminal_length(self):
        """Return the length of the terminal."""
        rows, cols = popen('stty size', 'r').read().split()
        return int(cols)

    def _parse_destination(self):
        # Check if the des is passed
        if self.des is not None:
            if path.isdir(self.des):
                self.des = path.join(self.des, self._get_name())
        else:
            self.des = self._get_name()

        # Put a check to see if file already exists.
        # Try to resume it if that's true
        if path.exists(self.des):
            rem_size = path.getsize(self.des)
            self._build_headers(rem_size)

    def _get_name(self):
        """Try to get the name of the file from the URL."""

        name = 'temp'
        temp_url = self.URL

        split_url = temp_url.split('/')

        for name in split_url[::-1]:
            if name != '':
                break

        return name

    def _format_size(self, size):
        """Format the passed size.

        If its more than an 1 Mb then return the size in Mb's
        else return it in Kb's along with the unit.
        """
        formatted_size = size
        dw_unit = 'bytes'

        if formatted_size > (1024 * 1024 * 1024):
            formatted_size = size / (1024 * 1024 * 1024)
            dw_unit = "GB's"
        elif formatted_size > (1024 * 1024):
            formatted_size = size / (1024 * 1024)
            dw_unit = "MB's"
        elif formatted_size > 1024:
            formatted_size = size / 1024
            dw_unit = "kb's"

        return (formatted_size, dw_unit)

    def _format_time(self, time_left):
        """Format the passed time depending."""

        if time_left > 3600:
            time_left = round(time_left / 3600)
            time_unit = 'h'
        elif time_left > 60:
            time_left = round(time_left / 60)
            time_unit = 'm'

        return time_left, time_unit

    def _get_speed_n_time(self, file_size_dl, beg_time, cur_time):
        """Return the speed and time depending on the passed arguments."""

        # Calculate speed
        speed = (file_size_dl / 1024) / (cur_time - beg_time)

        # Calculate time left
        time_left = round(((self.f_size - file_size_dl) / 1024) / speed)
        time_unit = 's'

        # Convert to min or hours as req
        if time_left > 3600:
            time_left = round(time_left / 3600)
            time_unit = 'h'
        elif time_left > 60:
            time_left = round(time_left / 60)
            time_unit = 'm'

        return speed, time_left, time_unit

    def download(self):
        try:
            self._parse_destination()

            # Download files with a progressbar showing the percentage
            self._preprocess_conn()
            WSTREAM = open(self.des, 'wb')

            formatted_file_size, dw_unit = self._format_size(self.f_size)
            print("Size: {} {}".format(round(formatted_file_size), dw_unit))
            print("Saving as: {}".format(self.des))

            file_size_dl = 0
            block_sz = 8192

            beg_time = time.time()
            while True:
                buffer = self.conn.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                WSTREAM.write(buffer)

                # Initialize all the variables that cannot be calculated
                # to ''
                speed = ''
                time_left = ''
                time_unit = ''
                percent = ''

                if self.f_size is not None:
                    speed, time_left, time_unit = self._get_speed_n_time(
                                                    file_size_dl,
                                                    beg_time,
                                                    cur_time=time.time()
                                                )
                    percent = file_size_dl * 100 / self.f_size

                # Get basename
                self.basename = path.basename(self.des)

                # Calculate amount of space req in between
                length = self._get_terminal_length()

                stuff_len = len(self.basename) + 13 + 17 + 7 + 26 + 3
                space = 0

                if stuff_len < length:
                    space = length - stuff_len
                elif stuff_len > length:
                    self.basename = self.basename[:(length - stuff_len) - 2] + '..'

                f_size_disp, dw_unit = self._format_size(file_size_dl)
                if self.f_size is not None:
                    status = r"%s %s %0.2f %s |%d kbps| ETA: %s %s |%-20s| |%3.2f%%|" % (self.basename, space * " ", f_size_disp, dw_unit, speed, time_left, time_unit, "-" * int(percent / 5), percent)
                else:
                    status = r"%s %s %0.2f %s" %(self.basename, space * " ", f_size_disp, dw_unit)
                sys.stdout.write('\r')
                sys.stdout.write(status)
                sys.stdout.flush()

            WSTREAM.close()

            print()
            return True
        except KeyboardInterrupt:
            sys.stdout.flush()
            print("Keyboard Interrupt passed. Exitting peacefully.")
            exit()
        except Exception as e:
            print("ERROR: {}".format(e))
            return False


if __name__ == "__main__":
    args = arguments()
    Download(args.URL, args.des).download()
