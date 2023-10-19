# WEBCARDS

We provide web-based generation of model cards and data sheets for machine learning transparency. This tool accelerates the development of solutions that validate artificial intelligence models and datasets against the Fairness, Ethics, Accountability, and Transparency (FEAT) principles. By strengthening trust and promoting the adoption of AI solutions, we aim to contribute to the responsible use of AI.

## Overview
Built with the Django framework, this web application leverages Google's [Model Card Toolkit](https://github.com/tensorflow/model-card-toolkit.git) as a basis for creating model cards. A customized library is created which can be found [here](https://github.com/mcmi-group/featai_lib.git).

The application allows users to input data and subsequently generates a model card as an HTML file. Users can upload datasets, model and graph files, which are then processed and incorporated into the model card. The uploaded files are temporarily stored in the `media/uploads` directory and are associated with a session key that's stored in the browser's cookies. Users have the option to delete these files, otherwise, they will be automatically removed after one hour.

We use SQLite3 as our database system due to its simplicity and speed, which are adequate for the current scale and complexity of our tool.

A CI/CD pipeline has been implemented using GitHub Actions for testing, building, and pushing updates to DockerHub. This ensures that data doesn't accumulate in the system, as files are either overwritten or deleted after usage.

For detailed documentation: https://webcards.readthedocs.io/en/latest/index.html
