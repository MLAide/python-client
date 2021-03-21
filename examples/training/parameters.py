import os


def get_project_key():
    project_key = os.getenv("MLAIDE_PROJECT_KEY")

    if project_key is None:
        project_key = input("Enter project key: ")

    return project_key


def get_experiment_key():
    experiment_key = os.getenv("MLAIDE_EXPERIMENT_KEY", None)

    if experiment_key is None:
        experiment_key = input("Enter experiment key: ")

    return experiment_key


def choose_between_cleaned_and_raw_data():
    return True if input("Use cleaned data (cleaned) or raw data (raw)? ") == "cleaned" else False


def get_alpha():
    alpha_input = input("alpha (default: 0.5): ")
    return float(alpha_input) if len(alpha_input) > 0 else 0.5


def get_l1_ratio():
    l1_ratio_input = input("l1 ration (default: 0.5): ")
    return float(l1_ratio_input) if len(l1_ratio_input) > 0 else 0.5
