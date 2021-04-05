import io
import cloudpickle


def serialize(model) -> io.BytesIO:
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
            return buffer
        # elif module_name.startswith("xgboost"):
        #     model_type = "xgboost"
        #     bytestream, method = ensure_bytestream(model)
        #     break
        # elif module_name.startswith("tensorflow.python.keras"):
        #     model_type = "tensorflow"
        #     tempf = tempfile.NamedTemporaryFile()
        #     if get_tensorflow_major_version() == 2:  # save_format param may not exist in TF 1.X
        #         model.save(tempf.name, save_format='h5')  # TF 2.X uses SavedModel by default
        #     else:
        #         model.save(tempf.name)
        #     tempf.seek(0)
        #     bytestream = tempf
        #     method = "keras"
        #     break


def deserialize(model: io.BytesIO) -> any:
    return cloudpickle.load(model)
