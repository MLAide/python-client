# Python Client Library for ML Aide

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
2. Install [pipenv](https://github.com/pypa/pipenv)
3. Optional - Install IDE: [PyCharm](https://www.jetbrains.com/pycharm/) 
or [Visual Studio Code](https://code.visualstudio.com/)

### Setup Environment
1. Install environment and download dependencies
    ```
   PIPENV_IGNORE_VIRTUALENVS=1
   pipenv install --dev
   ```
   
2. Activate environment
    ```shell script
    pipenv shell
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
python setup.py bdist_wheel
```

### Install
To install the package in the local environment in editable mode 
use the following command:
```
pipenv install -e .
```