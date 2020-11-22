import datetime
from typing import Dict, Optional, Union
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Artifact(object):
    name: str
    type: str
    created_at: datetime = None
    file: Optional[BytesIO] = None
    metadata: Optional[Dict[str, str]] = None
    run_key: Optional[int] = None
    run_name: Optional[str] = None
    updated_at: datetime = None
    version: Optional[int] = None

    def add_file(self, file: Union[str, BytesIO]):
        if isinstance(file, str):  # Read the file behind the string
            if file.startswith('http://') or file.startswith('https://'):  # The file must be downloaded
                pass
                # TODO: Download file

            else:  # The file must be read from filesystem
                path = Path(file)

                if path.is_file():  # check if it is only a single file
                    file_bytes = path.read_bytes()
                    self.file = BytesIO(file_bytes)

                elif path.is_dir():  # ... or is it a directory?
                    pass
                    # TODO: Read all files from directory

        else:  # The passed file is already of type BytesIO
            self.file = file
