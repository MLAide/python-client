from dataclasses import dataclass
from io import BytesIO


@dataclass
class InMemoryArtifactFile(object):
    file_name: str
    file_content: BytesIO
