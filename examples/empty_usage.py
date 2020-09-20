from modelversioncontrol.client import MvcClient, MvcOptions
from modelversioncontrol.api_client.errors import ApiResponseError

options = MvcOptions(api_token="")
mvc_client = MvcClient(options)

if __name__ == "__main__":

    try:
        active_experiment = mvc_client.start_new_experiment(
            project_id="01018351-0381-4220-86c5-c196b6259fc9",
            experiment_name="elasticnet-2")

        active_experiment.add_parameter("alpha", 0.6)
        active_experiment.add_parameter("l1_ratio", 0.5)
        active_experiment.add_metric("rmse", 0.9)
        active_experiment.add_metric("r2", 1)
        active_experiment.add_metric("mae", 0.98)

        # active_experiment.sklearn.add_model(lr, model_name="ElasticnetWineModel")

        active_experiment.set_completed_status()
    except ApiResponseError as error:
        print(error.response)
