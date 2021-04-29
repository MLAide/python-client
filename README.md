# Python Client Library for ML Aide
[![CI pipeline](https://github.com/MLAide/python-client/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/MLAide/python-client/actions/workflows/ci-pipeline.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MLAide_python-client&metric=alert_status)](https://sonarcloud.io/dashboard?id=MLAide_python-client)

## Run example scripts
In `examples/` you can find some python scripts as an example.
The shell scripts can be used for easier usage.

Run the following commands once in a terminal session
```shell script
cs/
source ./set_api_key.sh
```

After that you can use the following command to run the scripts
over and over again:
```shell script
./run_example.sh
```

## Contribution
### Prerequisites
1. Install [Python](https://www.python.org/)
2. Install [Python Poetry](https://python-poetry.org/docs/#installation)
3. Optional - Install IDE: [PyCharm](https://www.jetbrains.com/pycharm/) 
or [Visual Studio Code](https://code.visualstudio.com/)

### Setup Environment
1. Install environment and download dependencies
    ```shell
   poetry install
   ```
   
2. Activate environment
    ```shell
    poetry shell
    ```

### Run Tests
```
pytest
```

### Run Tests with Coverage
```
coverage run --branch --source mlaide -m pytest
coverage html
```

### Build
```
poetry build
```

### Publish (on PyPI)
```
poetry publish
```

## Links

- **Homepage:** https://mlaide.com
- **Quickstart:** https://docs.mlaide.com/start/quickstart/
- **Tutorial:** https://docs.mlaide.com/tutorial/introduction/
- **Documentation:** https://docs.mlaide.com/
