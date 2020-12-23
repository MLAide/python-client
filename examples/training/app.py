from parameters import get_project_key, get_experiment_key, get_alpha, get_l1_ratio
from data_ingest import run_ingest
from data_cleansing import run_cleansing
from training import run_training

if __name__ == "__main__":
    project_key = get_project_key()
    experiment_key = get_experiment_key()

    run_ingest(project_key, experiment_key)
    run_cleansing(project_key, experiment_key)
    run_training(project_key, experiment_key, True, 0.5, 0.5)
    run_training(project_key, experiment_key, True, 0.4, 0.4)
    run_training(project_key, experiment_key, True, 0.8, 0.3)
    run_training(project_key, experiment_key, False, 0.8, 0.8)
    run_training(project_key, experiment_key, False, 0.7, 0.9)
