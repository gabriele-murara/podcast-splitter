import math
import mimetypes
import os
from pathlib import Path

import eyed3
from pydub import AudioSegment

from classes.abstracts.has_logger import HasLogger


class SingleFileProcessor(HasLogger):

    __track = None
    __seconds = 0
    __output_directory = None

    def __init__(self, track, output_directory, seconds=60):
        super().__init__(self.__class__.__name__)
        self.__track = track
        self.__seconds = seconds
        self.__output_directory = output_directory

    def split_track(self):
        total_seconds = self.__track.info.time_secs
        msg = "Track {} is {} seconds long".format(
            self.__track.path, total_seconds
        )
        self.logger.info(msg)

        msg = "seconds is a {} and total_seconds is a {}".format(
            type(self.__seconds), type(total_seconds)
        )
        self.logger.info(msg)
        nr_of_split = math.ceil(total_seconds / self.__seconds)
        msg = "Start to split track into {} tracks of {} seconds".format(
            nr_of_split, self.__seconds
        )
        self.logger.info(msg)
        file_type = mimetypes.guess_type(self.__track.path)[0]
        _, file_extension = os.path.splitext(self.__track.path)
        if file_type is not None:
            # Estrai l'estensione dal tipo di file
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
        start_time = 0
        end_time = self.__seconds * 1000
        album_directory = "{}_splitted".format(base_filename)
        album_title = base_filename
        sub_directory = os.path.join(self.__output_directory, album_directory)
        if not os.path.exists(sub_directory):
            os.mkdir(sub_directory)
        for i in range(1, nr_of_split + 1):
            splitted_filename = "{}_{}.{}".format(
                base_filename, i, file_extension
            )
            destination_abs_path = os.path.join(
                sub_directory, splitted_filename
            )
            msg = "Start to split {}...".format(splitted_filename)
            self.logger.info(msg)
            splitted_track = audio_track[start_time:end_time]
            msg = "Export to {}...".format(destination_abs_path)
            self.logger.info(msg)
            splitted_track.export(destination_abs_path, format=file_type)
            track_title = "{}_{}".format(album_title, i)
            track_with_metadata = eyed3.load(destination_abs_path)
            track_with_metadata.tag.title = track_title
            track_with_metadata.tag.album = album_title
            track_with_metadata.tag.track_num = i
            track_with_metadata.tag.save()

            start_time += self.__seconds * 1000
            end_time += self.__seconds * 1000







