# Auto Driving Car Simulation

_GIC Take Home Assignment - Neel Modha (3rd March 2025)_

## Overview
This project is a command-line simulation of autonomous cars navigating a grid. Users can define the grid size, add cars with starting positions and movement commands, and then run a simulation to observe the final positions of the cars.

## Features added
- Code is able to handle invalid user inputs (e.g. trying to add cars outside of the simulation width/breadth, duplicate car names, etc.).
- Slightly expanded menu options to reset simulation (keeps grid, resets cars).
- Logic to disallow multiple car instantiation the same spot.
- If a car collides with multiple cars (at a single position), prints out an apprpriate message indicated all affected cars. 

## Development Environment
- **Operating System:** Windows
- **Python Version:** 3.12.9
- **Dependencies:** No external packages required – uses only built-in Python libraries.

## Running the Application
To run the main application:
```sh
python app.py
```

## Running Unit and Integration Tests Locally
The project includes a `test_app.py` file with unit and integration tests using `unittest`.
To execute the tests:
```sh
python -m unittest discover -s . -p "test_*.py"
```

## Automated Testing with GitHub Actions
Automated testing is set up via **GitHub Actions**, ensuring that tests run automatically on every push and pull request to the `main` branch.

Whenever changes are pushed to GitHub, tests run in a CI/CD pipeline using Python 3.12.9 on an Ubuntu-based runner.

For more details, check the **Actions** tab in the repository.

---

