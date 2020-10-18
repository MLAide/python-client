from modelversioncontrol.client import MvcClient, MvcOptions
from modelversioncontrol._api_client.errors import ApiResponseError

options = MvcOptions(api_token="")
mvc_client = MvcClient(options)

if __name__ == "__main__":

    try:
        active_experiment = mvc_client.start_new_run(
            project_key="my-first-project",
            run_name="elasticnet-2")

        active_experiment.log_parameter("alpha", 0.7)
        active_experiment.log_parameter("l1_ratio", 0.5)
        active_experiment.log_metric("rmse", 0.8)
        active_experiment.log_metric("r2", 1)
        active_experiment.log_metric("mae", 0.98)

        # active_experiment.sklearn.add_model(lr, model_name="ElasticnetWineModel")

        active_experiment.set_completed_status()
    except ApiResponseError as error:
        print(error.response)
