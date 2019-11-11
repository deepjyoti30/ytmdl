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

    def __init__(self, URL, des=None, icon_done="▓", icon_left="░"):
        self.URL = URL
        self.des = des
        self.headers = {}
        self.f_size = 0
        self.done_icon = icon_done
        self.left_icon = icon_left

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
        map_unit = {0: 'bytes', 1: "KB's", 2: "MB's", 3: "GB's"}
        formatted_size = size

        no_iters = 0
        while formatted_size > 1024:
            no_iters += 1
            formatted_size /= 1024

        return (formatted_size, map_unit[no_iters])

    def _get_size_orig_terms(self, size):
        """Return the size in original files terms."""

    def _format_time(self, time_left):
        """Format the passed time depending."""
        unit_map = {0: 's', 1: 'm', 2: 'h'}

        no_iter = 0
        while time_left > 60:
            no_iter += 1
            time_left /= 60

        return time_left, unit_map[no_iter]

    def _format_speed(self, speed):
        """Format the speed."""
        unit = {0: 'Kb/s', 1: 'Mb/s', 2: 'Gb/s'}

        inc_with_iter = 0
        while speed > 1000:
            speed = speed / 1000
            inc_with_iter += 1

        return speed, unit[inc_with_iter]

    def _get_speed_n_time(self, file_size_dl, beg_time, cur_time):
        """Return the speed and time depending on the passed arguments."""

        # Calculate speed
        speed = (file_size_dl / 1024) / (cur_time - beg_time)
        speed, s_unit = self._format_speed(speed)

        # Calculate time left
        time_left = round(((self.f_size - file_size_dl) / 1024) / speed)
        time_left, time_unit = self._format_time(time_left)

        return speed, s_unit, time_left, time_unit

    def _get_bar(self, status, length, percent):
        """Calculate the progressbar depending on the length of terminal."""

        map_bar = {
                    40: r"|%-40s|",
                    20: r"|%-20s|",
                    10: r"|%-10s|",
                    5: r"|%-5s|",
                    2: r"|%-2s|"
        }
        # Till now characters present is the length of status.
        # length is the length of terminal.
        # We need to decide how long our bar will be.
        cur_len = len(status) + 2 + 4  # 2 for bar and 6 for percent

        reduce_with_each_iter = 40
        while reduce_with_each_iter > 0:
            if cur_len + reduce_with_each_iter > length:
                reduce_with_each_iter = int(reduce_with_each_iter / 2)
            else:
                break

        # Add space.
        space = length - (len(status) + 2 + reduce_with_each_iter + 5)
        status += r"%s" % (" " * space)

        if reduce_with_each_iter > 0:
            # Make BOLD
            status += "\033[1m"
            # Add color.
            status += "\033[1;34m"
            done = int(percent / (100 / reduce_with_each_iter))
            status += r"|%s%s|" % (self.done_icon * done, self.left_icon * (reduce_with_each_iter - done))

        status += "\033[0m"
        return status

    def download(self):
        try:
            self._parse_destination()

            # Download files with a progressbar showing the percentage
            self._preprocess_conn()
            WSTREAM = open(self.des, 'wb')

            formatted_file_size, dw_unit = self._format_size(self.f_size)
            print("Size: {} {}".format(round(formatted_file_size), dw_unit))
            print("Saving as: {}".format(self.des))
            self.orig_dw_unit = dw_unit

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
                    speed, s_unit, time_left, time_unit = self._get_speed_n_time(
                                                    file_size_dl,
                                                    beg_time,
                                                    cur_time=time.time()
                                                )
                    percent = file_size_dl * 100 / self.f_size

                # Get basename
                self.basename = path.basename(self.des)

                # Calculate amount of space req in between
                length = self._get_terminal_length()

                f_size_disp, dw_unit = self._format_size(file_size_dl)
                if self.f_size is not None:
                    # status = r"%s %s" % (self.basename, space * " ")
                    status = r"%-9s" % ("%s %s" % (round(f_size_disp), dw_unit))
                    status += r"| %-3s %s || " % ("%s" % (round(speed)), s_unit)
                    status += r"ETA: %s %s " % (round(time_left), time_unit)
                    status = self._get_bar(status, length, percent)
                    status += r" %-4s" % ("{}%".format(int(percent)))
                else:
                    status = r"%0.2f %s" % (f_size_disp, dw_unit)
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
