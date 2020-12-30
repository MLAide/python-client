from dataclasses import dataclass


@dataclass
class ArtifactFile(object):
    fileId: str
    fileName: str
