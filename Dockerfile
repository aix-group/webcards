# Use an official Python runtime as a parent image
FROM python:3.8

# setup environment variable  
ENV DockerHOME=/home/app/webapp 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory  
RUN mkdir -p $DockerHOME 

# where your code lives  
WORKDIR $DockerHOME  

# copy whole project to your docker home directory. 
COPY . $DockerHOME   

# run this commands to install all dependencies  
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install --upgrade utils/model_card_toolkit-2.0.0.dev0-py3-none-any.whl

# Run migrations
# RUN python manage.py makemigrations 
# RUN python manage.py migrate --fake

# Unzip the database
RUN unzip db.sqlite3.zip

# port where the Django app runs  
EXPOSE 8000 

# start server  
CMD python manage.py runserver  