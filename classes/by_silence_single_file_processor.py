import mimetypes
import os
from pathlib import Path

import eyed3
from pydub import AudioSegment
from pydub.silence import split_on_silence

from classes.abstracts.has_logger import HasLogger


class BySilenceSingleFileProcessor(HasLogger):

    __track = None
    __output_directory = None
    __verbose = False

    def __init__(
            self,
            track,
            output_directory,
            log_filename="",
            verbose=False
    ):
        super().__init__(self.__class__.__name__, log_filename, verbose)
        self.__verbose = verbose
        self.__track = track
        self.__output_directory = output_directory

    def split_track(self):
        total_seconds = self.__track.info.time_secs
        msg = "Track {} is {} seconds long".format(
            self.__track.path, total_seconds
        )
        self.logger.info(msg)

        msg = "Start to split track '{}' by silence."
        msg += "Output is saved to {}"
        msg = msg.format(
            self.__track.path,
            self.__output_directory
        )
        self.logger.info(msg)
        if not self.__verbose:
            print(msg)
        file_type = mimetypes.guess_type(self.__track.path)[0]
        _, file_extension = os.path.splitext(self.__track.path)
        if file_type is not None:
            # Get extension from file's type
            if file_type == 'audio/mpeg':
                file_extension = 'mp3'
                file_type = 'mp3'
            else:
                file_extension = file_type.split("/")[-1]
                file_type = file_extension
        elif file_extension is not None:
            file_type = file_extension
        else:
            msg = "Unable to detect file_type and extension for {}. Use the "
            msg += "default .mp3"
            self.logger.warning(msg.format(self.__track.path))
            file_extension = 'mp3'
            file_type = file_extension
        base_filename = Path(self.__track.path).stem
        audio_track = AudioSegment.from_file(self.__track.path)
        chunks = split_on_silence(
            audio_track,

            # split on silences longer than 1000ms (1 sec)
            min_silence_len=1000,

            # anything under -16 dBFS is considered silence
            silence_thresh=-16,

            # keep 200 ms of leading/trailing silence
            keep_silence=200
        )

        album_directory = "{}_splitted".format(base_filename)
        album_title = base_filename
        sub_directory = os.path.join(self.__output_directory, album_directory)
        if not os.path.exists(sub_directory):
            os.mkdir(sub_directory)
        self.logger.info("Sound splitted in {} chunks".format(len(chunks)))

        # now recombine the chunks so that the parts are at least 90 sec long
        target_length = 90 * 1000
        output_chunks = [chunks[0]]
        self.logger.info("Start to recombine chunks...")
        for chunk in chunks[1:]:
            self.logger.info("process next chunk...")
            if len(output_chunks[-1]) < target_length:
                output_chunks[-1] += chunk
            else:
                # if the last output chunk is longer than the target length,
                # we can start a new one
                output_chunks.append(chunk)

        i = 0
        self.logger.info("Start to export chunks...")
        for c in output_chunks:
            i += 1
            splitted_filename = "{}_{:02d}.{}".format(
                base_filename, i, file_extension
            )
            destination_abs_path = os.path.join(
                sub_directory, splitted_filename
            )
            msg = "Exporting {} chunk to {}...".format(i, splitted_filename)
            self.logger.info(msg)

            track_title = "{}_{}".format(album_title, i)
            c.export(destination_abs_path, format=file_type)
            track_with_metadata = eyed3.load(destination_abs_path)
            track_with_metadata.tag.title = track_title
            track_with_metadata.tag.album = album_title
            track_with_metadata.tag.track_num = i
            track_with_metadata.tag.save()
        self.logger.info("Done!")
