.. WebCards documentation master file, created by
   sphinx-quickstart on Wed Sep 20 09:31:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

WebCards Documentation
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Welcome to the documentation of the WebCards tool. Here you can find useful information about the app, its logic, and its use. WebCards is a tool for creating and sharing model cards and datasheets, which are documents that provide context and transparency for machine learning tasks. 
The tool is under development and heavy testing. If you find any bugs or have any suggestions, please create an issue in `GitHub <https://github.com/mcmi-group/webcards>`_ page.

Overview
============

Built with the Django framework, this web application leverages Google's `Model Card Toolkit <https://github.com/tensorflow/model-card-toolkit.git>`_ as a basis for creating model cards. A customized library is created which can be found `here <https://github.com/mcmi-group/featai_lib.git>`_.

The application allows users to input data and subsequently generates a model card as an HTML file. Users can upload datasets, model and graph files, which are then processed and incorporated into the model card. The uploaded files are temporarily stored in the `media/uploads` directory and are associated with a session key that's stored in the browser's cookies. Users have the option to delete these files, otherwise, they will be automatically removed after one hour.

We use SQLite3 as our database system due to its simplicity and speed, which are adequate for the current scale and complexity of our tool.

A CI/CD pipeline has been implemented using GitHub Actions for testing, building, and pushing updates to DockerHub. This ensures that data doesn't accumulate in the system, as files are either overwritten or deleted after usage.


Getting Started
===============

The tool is currently in the early stages of production. Once it's ready for public use, the link will be provided here.

To deploy the tool locally, follow these steps:

1. **Clone the Repository**:
   
   .. code-block:: bash
   
      git clone https://github.com/mcmi-group/feat_ai.git

2. **Create a New Virtual Environment**:
   
   .. code-block:: bash
   
      conda create --name webcards python=3.8

3. **Activate the Virtual Environment**:
   
   .. code-block:: bash
   
      conda activate webcards

4. **Navigate to the Web App Directory**:
   
   .. code-block:: bash
   
      cd rai_webapp

5. **Install the Required Packages**:
   
   .. code-block:: bash
   
      pip install -r requirements.txt

6. **Install the Model Card Toolkit**:
   
   .. code-block:: bash
   
      pip install --upgrade utils/model_card_toolkit-2.0.0.dev0-py3-none-any.whl

7. **Run the Server**:
      
   .. code-block:: bash
        
      unzip db.sqlite3.zip
      
      python manage.py runserver

After following these steps, you should have the tool set up and ready to run locally.


Technical Overview
==================

Currently, the tool can generate model cards and datasheets. Central to the model card generation is the `ModelCard` dataclass, which serves as a blueprint for the entire card. This dataclass is structured hierarchically:

.. code-block::

   ModelCard Dataclass
   │
   ├── Section 1 (Subclass of ModelCard)
   │   ├── Field 1.1 (Subclass of Field)
   │   │   ├── Subfield 1.1.1 (Subclass of Field 1.1)
   │   │   ├── Subfield 1.1.2
   │   │   └── ...
   │   │
   │   ├── Field 1.2
   │   └── ...
   │
   ├── Section 2
   │   ├── Field 2.1 (Subclass of Field)
   │   │   ├── Subfield 2.1.1 (Subclass of Field 2.1)
   │   │   └── ...
   │   │
   │   ├── Field 2.2
   │   └── ...
   │
   └── ...

Each section in the `ModelCard` dataclass contains fields, which can further have subfields, allowing for a detailed and granular representation of the model card's content.

For datasheets, the process is streamlined. User responses are directly rendered into HTML, bypassing the dataclass representation.

User inputs, collected through the website, are populated into these data structures. The `ModelCardGenerator` then processes these inputs, culminating in the creation of a model card ready for export.

Through the documentation especially for the developer guider, it is recommended to check the official django documentation for more information about the framework. The documentation can be found `here <https://docs.djangoproject.com/en/3.2/>`_.

.. toctree::
   :caption: Developer Guide
   :maxdepth: 2

   backend/customization
   backend/database
   backend/django_backend
   frontend/views
   frontend/html_structure
   backend/session


.. toctree::
   :caption: User Guide
   :maxdepth: 2

   model_card/usage
   model_card/example_usage
   datasheet/usage
