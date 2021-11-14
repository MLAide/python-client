import io
from typing import Any, Callable, Union
import cloudpickle
import tempfile
from pathlib import Path


def serialize(model: Any, save_callback: Callable[[Union[str, io.BytesIO], str], None]):
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

            save_callback(buffer, 'model.pkl')
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
                        relative_path = str(path.relative_to(tmpdir_path))
                        save_callback(str(path), relative_path)

            break
