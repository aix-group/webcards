# A web application for FEAT principles

This web tool seeks to accelerate the development of solutions that validate artificial intelligence models and datasets against the fairness, ethics, accountability and transparency (FEAT) principles, to strengthen trust and promote greater adoption of AI solutions.

## Instructions to deploy locally: Create a virtual environment and install the dependencies

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

pip install --upgrade model_card_toolkit-2.0.0.dev0-py3-none-any.whl

```

### Unzip the database file and run the server

```sh
unzip db.sqlite3.zip

python manage.py runserver

```
###

now click [here](http://localhost:8000/feat_ai/) to open the server.
