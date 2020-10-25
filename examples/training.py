import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from modelversioncontrol.client import MvcClient, MvcOptions

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
options = MvcOptions(api_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InI5Y2F0QVVUdnlmRzZpTHF5ZFBCaiJ9.eyJpc3MiOiJodHRwczovL212Yy1kZXYuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNTNhYjY3NDJlMzQ1MDA2ZGIyYjhkMiIsImF1ZCI6Imh0dHBzOi8vYXBpLm12Yy5pbyIsImlhdCI6MTYwMzYzMDU0MCwiZXhwIjoxNjAzNzE2OTQwLCJhenAiOiIyN1o0S2dFOHZUdU1vNFZIMDg3NG81QzQyTTVzY21OdiJ9.EsHhkfSaTRrQOdOGVyGtEYewsPCd-jfA_a_mLA1hTP1glljfMNtEYd8A8ZG5SGKGdT6rEU2wghIduxL98Ke3jqkencmToHcCyK22FnoXcLMH6wh4Ex7RLK4AdD0AiO71x2tpKUxiIyqn6ypfnqnXxk9hjJ28tE6dDGRS7M2gEN-jX4Y0L7O2v_9sArGBm3hF4SMAdgM1qH8XWm34zhtYzwakiebthy4Ydv1JgNNfm7LwpGb4JGQv-25rPB652-z0uD-iTtpCbkRlY9Kp2N4LGZtEOHhDqORGyooL3xn6DPDm5LtD7pTGbEOBaDRls5MXRT1gJJq_4fPqb7FXrlVneA")
mvc_client = MvcClient(options)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = (
        "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    )
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

    run = mvc_client.start_new_run(project_key="project-x",
                                   experiment_key=None,  # create new experiment for this run
                                   run_name="wine-quality-sample")

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    run.log_parameter("alpha", alpha)
    run.log_parameter("l1_ratio", l1_ratio)
    run.log_metric("rmse", rmse)
    run.log_metric("r2", r2)
    run.log_metric("mae", mae)

    run.log_model(lr, model_name="ElasticnetWineModel")

    run.set_completed_status()
