# A web application for FEAT principles

This web tool seeks to accelerate the development of solutions that validate artificial intelligence models and datasets against the fairness, ethics, accountability and transparency (FEAT) principles, to strengthen trust and promote greater adoption of AI solutions.

## Introduction
The web application tool developed using Django framework. As a baseline to create model card, Google's [model card toolkit](https://github.com/tensorflow/model-card-toolkit.git) is used. Customized library can be foung [here](https://github.com/mcmi-group/featai_lib.git).


The tool takes several inputs from the user then export the model card as html file. User has the chance to upload dataset, model and graph files to be utilized in the model card creation process. The uploaded files are then stored in the ```media/uploads``` folder with session key. This 
session key is stored in the cookies of the used browser. User has the chance the delete the files. Otherwise files will be deleted after one hour.

We use SQLlite3 database as it is provides simple and fast database solution. At this point, the database is not big and the tool is simple. Thus, SQLlite3 should be ok to use.

Lastly, a small CI/CD pipeline implemented to test, build and push to DockerHub using GitHub Actions. There is no issues stacking up data when using the tool as the files either overwritten or deleted after the use of the tool.

## To run the Docker image
```sh
docker pull sperbaha/featai:latest

docker run -d -p 8000:8000 --name featai_cont sperbaha/featai:latest

```
After this point, some additional steps should be taken in the context of production environment.

## Instructions to deploy locally

-Create a new virtual environment:
```sh
conda create --name featai python=3.8
```
-Activate the virtual environment:
```sh
conda activate featai
```
-Installation:
```sh

git clone https://github.com/mcmi-group/rai_webapp.git

cd rai_webapp

pip install django

pip install -r requirements.txt

pip install --upgrade utils/model_card_toolkit-2.0.0.dev0-py3-none-any.whl

```

### Unzip the database file and run the server

```sh
unzip db.sqlite3.zip

python manage.py runserver

```
###

now click [here](http://localhost:8000/feat_ai/) to open the server.
