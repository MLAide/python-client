import io
import os
from typing import Any, Collection, Union
import cloudpickle
import tempfile
from pathlib import Path

from mlaide.model.artifact_file import ArtifactFile

from mlaide.model import InMemoryArtifactFile, LocalArtifactFile


def serialize(model: Any) -> Collection[Union[InMemoryArtifactFile, LocalArtifactFile]]:
    files = []

    for class_obj in model.__class__.__mro__:
        module_name = class_obj.__module__
        if not module_name:
            continue
        # elif module_name.startswith("torch"):
        #     model_type = "torch"
        #     bytestream, method = ensure_bytestream(model)
        #     break
        elif module_name.startswith("sklearn"):
            buffer = io.BytesIO()
            cloudpickle.dump(model, buffer)
            buffer.seek(0)

            files.append(InMemoryArtifactFile(file_name='model.pkl', file_content=buffer))
            break
        # elif module_name.startswith("xgboost"):
        #     model_type = "xgboost"
        #     bytestream, method = ensure_bytestream(model)
        #     break
        elif module_name.startswith("keras.engine.training"):
            with tempfile.TemporaryDirectory() as tmpdirname:
                model.save(tmpdirname, save_format='tf')

                tmpdir_path = Path(tmpdirname)
                pathlist = tmpdir_path.rglob('*')
                for path in pathlist:
                    if (path.is_file()):
                        file_name = os.path.split(path.absolute())
                        files.append(LocalArtifactFile(file_name=file_name, file_path=path))

            break

    return files
