import json
import os
from dataclasses import asdict

from config import path_config, settings
from consts.consts import TEXT_FILE_EXTENSION, LAST_NAME_DEFAULT_WORDS_SEPARATION, LAST_NAME_WANTED_WORDS_SEPARATION
from models.output import Output
from write.writer import Writer


class FolderWriter(Writer):

    @staticmethod
    def get_file_name(output: Output):
        first_name = output.studentDetails.firstName.title()
        last_name = output.studentDetails.lastName.title().replace(LAST_NAME_DEFAULT_WORDS_SEPARATION, LAST_NAME_WANTED_WORDS_SEPARATION)
        file_name = f"{first_name}_{last_name}{TEXT_FILE_EXTENSION}"

        return file_name

    def write(self, output: Output):
        folder_path = path_config.STUDENTS_DIR_PATH

        if settings.ENV == "test":
            folder_path = path_config.TEST_STUDENTS_DIR_PATH

        complete_path = os.path.join(folder_path, FolderWriter.get_file_name(output))

        with open(complete_path, "w") as file:
            data = json.dumps(asdict(output, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}), indent=4)
            file.write(data)

        print(f"[X] Created text file for: {output.studentDetails.fullName}")
