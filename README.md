# WEBCARDS

We provide web-based generation of model cards and data sheets for machine learning transparancy. This tool accelerates the development of solutions that validate artificial intelligence models and datasets against the Fairness, Ethics, Accountability, and Transparency (FEAT) principles. By strengthening trust and promoting the adoption of AI solutions, we aim to contribute to the responsible use of AI.

## Overview
Built with the Django framework, this web application leverages Google's [Model Card Toolkit](https://github.com/tensorflow/model-card-toolkit.git) as a basis for creating model cards. A customized library is created which can be found [here](https://github.com/mcmi-group/featai_lib.git).

The application allows users to input data and subsequently generates a model card as an HTML file. Users can upload datasets, model and graph files, which are then processed and incorporated into the model card. The uploaded files are temporarily stored in the `media/uploads` directory and are associated with a session key that's stored in the browser's cookies. Users have the option to delete these files, otherwise, they will be automatically removed after one hour.

We use SQLite3 as our database system due to its simplicity and speed, which are adequate for the current scale and complexity of our tool.

A CI/CD pipeline has been implemented using GitHub Actions for testing, building, and pushing updates to DockerHub. This ensures that data doesn't accumulate in the system, as files are either overwritten or deleted after usage.

## Docker Deployment

To run the Docker image:

```sh
docker pull sperbaha/featai:latest

docker run -d -p 8000:8000 --name featai_cont sperbaha/featai:latest

```
For a production environment, additional deployment steps may be necessary.

## Instructions to deploy locally

-Create a new virtual environment:
```sh
conda create --name webcards python=3.8
```
-Activate the virtual environment:
```sh
conda activate webcards
```
-Installation:
```sh

git clone https://github.com/mcmi-group/feat_ai.git

cd rai_webapp

pip install -r requirements.txt

pip install --upgrade utils/model_card_toolkit-2.0.0.dev0-py3-none-any.whl

```

### Unzip the database file and run the server

```sh
unzip db.sqlite3.zip

python manage.py runserver

```
###

For detailed documentation: https://webcards.readthedocs.io/en/latest/index.html

now click [here](http://localhost:8000/feat_ai/) to open the server.
