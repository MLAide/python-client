import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from modelversioncontrol.client import MvcClient, MvcOptions
from modelversioncontrol.artifact import Artifact

import logging
import http.client

httpclient_logger = logging.getLogger("http.client")


def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    logging.basicConfig(level=logging.DEBUG)

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1


httpclient_logging_patch()
options = MvcOptions(api_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InI5Y2F0QVVUdnlmRzZpTHF5ZFBCaiJ9.eyJpc3MiOiJodHRwczovL212Yy1kZXYuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDI5MTMzNDIwN2QxMDA2ZGVjNWFmMCIsImF1ZCI6WyJodHRwczovL2FwaS5tdmMuaW8iLCJodHRwczovL212Yy1kZXYuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwNTQ0ODI3OCwiZXhwIjoxNjA1NTM0Njc4LCJhenAiOiIyN1o0S2dFOHZUdU1vNFZIMDg3NG81QzQyTTVzY21OdiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.zIlJWZCBb5LCIjCMH1fFNzvuetBbfj_VapjJz5LOIQunNeCjdXCat5CMe9hE6eoiuJZUezmM8R8RvhC5Ww2wr2_IppsuEIQFZsSKRPQUaLcIppquCp9E1PaJq9OgZn0IV5EteZ8lccrMejFFCyAPodwh_OGckprG4j0r83lOZmhFffl_UtsTTivFO2KmVLnkaIm8P6jeoj7OTPAqfVGNSO_tvVpwwQoVwNGG2-VBpmUNSiN-5F-esG-fbG3NP979MFfHjgfPKH71TIJZ25vXfh9m4zn8mkDkwISOCOZW5Huol0eTnMkHle8qCps_ZGCMy3I2BfiCec7IonzefejQmw")
mvc_client = MvcClient(options)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    data = pd.read_csv(csv_url, sep=";")

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    ##################
    # Create a new run
    run = mvc_client.start_new_run(project_key="projekt",
                                   experiment_key=None,  # create new experiment for this run
                                   run_name="wine-quality-sample")
    ###############################
    # Attach the dataset to the run
    artifact = Artifact(name="winequality-red.csv", type="dataset")
    artifact.add_file('./winequality-red.csv')
    artifact.metadata = {
        "source": csv_url
    }
    run.log_artifact(artifact)

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
