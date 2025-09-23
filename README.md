This is a project for an automation framework for E2E testing, REST APIs, and DBs (relational/non-relational).
To run tests, download this project and follow the steps below:
- python -m venv .venv - create a virtual environment folder for installing the necessary packages
- source .venv/bin/activate - switch to the project's virtual environment
- pip install -r requirements.txt - install all necessary dependencies for running the project in a virtual environment
- pylint <file_or_folder_path> - check code purity (optional)
- pytest -m crit tests/ - run all E2E tests
- pytest -m crit tests/test_login_page.py - run all E2E tests from the file test_login_page.py
- pytest -m crit tests/test_login_page.py::test_sign_in - run the test_sign_in test from the file test_login_page.py


Possible problems:
- The backend container won't start.
Solution:
If you have a MacBook, temporarily disable AirPlay.
You can also check what's using port 5000 and disable that service for now.

Or find the PID of the running service.
- lsof -i :5000

Kill the process.
- kill < your PID>