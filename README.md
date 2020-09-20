# Python SDK - Model Version Control

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

### Run Test
```
python setup.py pytest
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