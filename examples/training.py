import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from modelversioncontrol.client import MvcClient, MvcOptions

options = MvcOptions(api_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InI5Y2F0QVVUdnlmRzZpTHF5ZFBCaiJ9.eyJpc3MiOiJodHRwczovL212Yy1kZXYuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDI5MTMzNDIwN2QxMDA2ZGVjNWFmMCIsImF1ZCI6WyJodHRwczovL2FwaS5tdmMuaW8iLCJodHRwczovL212Yy1kZXYuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwMjAwOTI0OSwiZXhwIjoxNjAyMDk1NjQ5LCJhenAiOiIyN1o0S2dFOHZUdU1vNFZIMDg3NG81QzQyTTVzY21OdiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.MzLyfuCYbqHwdrTcvnZYCuo3Xlj3gn8vdKdVaKUdQpSQSj3m9oIyJvRVKl0bBv0aAF-ZYaCUaNETGaiANtVKpvgTAUw84Dtz-6fdDrVleV_xKo_lDpWO_Lu9d6GRrQQYxAxQDvbYm0DEgBwm8drRlRjKHL7DyMBQ9ausXzKTKJqE0pcJarNZX__MNc0NereXLBQBpkyYwlXfpI6MwYoLxavpJ4wvxRFt3raRk4Az8NMRSTj2yJk2pYV8UDhCcG2nUbaGEdPqnqydaiEwmp5mDgmPBRs7UzKJFnY1EacWsxkO-w-_4wsIkin3scztXSaFtNRw34d9r51yo5NpeOHseg")
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

    run = mvc_client.start_new_run(project_id="0cf0a543-76a9-44f2-91ca-6e123ae8a7cf", experiment_key=None, run_name="wine-quality-sample")

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
