# CSI3335 Project Virtual Environment

This repository provides a virtual environment setup with specified dependencies for student projects in the CSI3335 course. **Please use Python 3.10 and above**

## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/sanjelarun/csi3335-project-venv.git
    cd csi3335-project-venv
    ```

2. **Create a Virtual Environment**

    **For Windows**

    ```bash
    python -m venv project_env
    ```

    **For Linux/MacOs**

    ```bash
    python3 -m venv project_env
    ```

3. **Activate the Virtual Environment**

    **For Windows**

    ```bash
    .\project_env\Scripts\activate
    ```

    **For Linux/MacOs**

    ```bash
    source project_env/bin/activate
    ```

4. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the virtual environment is activated and dependencies are installed, you can start working on your project within this environment. Remember to deactivate the virtual environment once you're done:

```bash
deactivate
```

## Starting the Flask dev server

After activating the virtual environment and installing the required dependencies, you're ready to get started. To start the development server, just run

```bash
flask run --debug
```

The debug flag is not required, but will let flask know to restart the server anytime changes are made so you don't have to keep shutting it down and booting it back up.
