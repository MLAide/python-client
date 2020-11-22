import sys
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from modelversioncontrol.artifact_ref import ArtifactRef
from modelversioncontrol.client import MvcClient

experiment_key = os.getenv("MVC_EXPERIMENT_KEY", None)
mvc_client = MvcClient()


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    np.random.seed(40)

    # Read the wine-quality csv file from filesystem
    data = pd.read_csv("./winequality-red.csv", sep=";")

    ##################
    # Create a new run
    # Also attach the input artifacts to this run
    artifact_ref = ArtifactRef(name="winequality-red.csv", version=1)
    run = mvc_client.start_new_run(project_key="projekt",
                                   experiment_key=experiment_key,
                                   run_name="wine-quality-model-training",
                                   used_artifacts=[artifact_ref])

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    # Train/fit the model
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    # Test the trained model
    predicted_qualities = lr.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    ############################
    # Log parameters and metrics
    run.log_parameter("alpha", alpha)
    run.log_parameter("l1_ratio", l1_ratio)
    run.log_metric("rmse", rmse)
    run.log_metric("r2", r2)
    run.log_metric("mae", mae)

    #######################
    # Log the trained model
    run.log_model(lr, model_name="ElasticnetWineModel")

    ##########################
    # Set the run as completed
    run.set_completed_status()
