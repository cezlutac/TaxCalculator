# Info

This is a simple tax calculator app that communicates with an existing API endpoint in order to calculate the total income tax for an input salary and tax year.
The `ptsdocker16/interview-test-server` app, used for fetching tax bracket information, is hosted on port 5000, while the calculator app itself `docker.io/cezlutac/tax-calculator` is hosted on port 4000.
Once both containers are launched, the behaviour can be tested both by unit tests through `python3 ./tests.py` or through a command line interface using `python3 ./calculate.py`

Note: Networking between Docker containers can be finnicky sometimes, especially depending on how Docker is installed on your system. If the Docker container for the tax-calculator doesn't work right, please see the section on [Dockerless instructions to setup & run the app](#dockerless-instructions-to-setup--run-the-app)

# Easy setup

```
docker pull ptsdocker16/interview-test-server
docker pull docker.io/cezlutac/tax-calculator
docker run --init -p 5000:5000 -d --net=bridge -it ptsdocker16/interview-test-server
docker run --init -p 4000:4000 -d --net=bridge --add-host=host.docker.internal:172.17.0.1 -it docker.io/cezlutac/tax-calculator
```

# Running unit tests

python3 ./tests.py

# Command-line requests

python3 ./calculate.py

# Known bugs

Since both docker containers are running on localhost, they will use 'host.docker.internal' to communicate with eachother.
This should work by default on Windows and Mac, though Linux may need to run the docker container with `--add-host host.docker.internal:172.17.0.1` as per
https://docs.docker.com/desktop/mac/networking/#use-cases-and-workarounds

If this does not work for you, you will need to run the tax calculator app without docker so that it can communicate with the existing app.

## Dockerless instructions to setup & run the app

Set up the python environment

```
cd app
python3 -m venv ./env
source env/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask run --port=4000
```

Note: on Windows, you may need to enable the execution of venv with 'powershell Set-ExecutionPolicy RemoteSigned' in an admin instance of cmd.exe
Also on Windows, the venv command becomes `.\env\Scripts\activate` instead of `source env/bin/activate`

# Building a new container

```
cd app
rm -rf ./env ./__pycache__
docker build -f Dockerfile -t tax-calculator:1 .
```


---------------------------

# Original Instructions

Instructions

We’ve created a mock API that returns marginal tax rates based on the inputted year. The API is accessible via a GET request to http://localhost:5000/tax-calculator/brackets/{tax_year}, which returns a JSON object that includes income tax brackets and the corresponding tax rates. To run the mock API server:

docker pull ptsdocker16/interview-test-server

docker run --init -p 5000:5000 -it ptsdocker16/interview-test-server

Your task is to build an application that queries our mock API and calculates the total income tax for an inputted salary and tax year. You may refer to this resource for context on how to calculate total income tax using margin tax rates: https://investinganswers.com/dictionary/m/marginal-tax-rate#:~:text=To%20calculate%20marginal%20tax%20rate,bracket%20your%20current%20income%20falls

The application you’re building should have an HTTP API with an endpoint that takes an annual income and the tax year as parameters. The appropriate type of params (query vs body param vs URL etc.) is to be determined by you. Your endpoint should return a JSON object with the result of the calculation.


Be aware that we’ve baked in two errors in our mock API — you may handle them and anything else you see fit to handle accordingly:

    only years 2019 and 2020 are supported

    the API throws errors randomly


IMPORTANT:

    Design the application as you would a production app that you and your team are collaborating on. Your result should not be a proof of concept and should focus more on the assessment criteria listed above than on working code.

    You may stumble upon instructions/requirements for the assignment returned in the Docker image. Please ignore these instructions and only refer to the evaluation criteria and instructions included in this email.
