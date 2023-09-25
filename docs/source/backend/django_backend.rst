Django Backend
==============

Introduction
------------

The Django backend of this project serves as the linchpin, handling data management, business logic, and interfacing with the database. Built upon the robust MVC (Model-View-Controller) architectural pattern, which Django terms as the MVT (Model-View-Template) pattern, our backend ensures a separation of concerns:

- **Models**: Define the data structures and the database schema. They act as the single source of truth for data and provide various methods and utilities to query the database.
  
- **Views**: Responsible for processing user requests and returning appropriate responses. In Django, views take the web request and return a web response, often by fetching or updating the data using models and combining it with templates.
  
- **Templates**: Django's way of generating dynamic HTML content. It's where data is presented, and user interfaces are formed.


Models
------

Models can be found in the `models.py` file under the main app folder which is `mc_and_datasheet` . There are 8 models implemented in this project: five for Model Cards and three for Datasheets. The Model Card models are as follows:

- **MC_section**: Represents all the sections in the model card. It has a name, click_count, section description and session id variable. 
- **Field**: Represents all the field in the model card. It is connected to the MC_section with foreignkey so that when section is queried fields can also be extracted.
- **CardSectionData**: An intermediate model that is use to store the data of the fields of one section in the model card. 
- **CardData**: It is the reflection of the all model card data in the database. It stores the model card data as json fields and has variable `carddata_session`to store the session id.
- **File**: It is used to store the file uploaded by the user. It has a file field and a session id variable.

- **dt_section**: Same as MC_section but for datasheet.
- **dt_field**: Same as Field but for datasheet.
- **CardDataDatasheet**: Same as CardData but for datasheet.


Models are like mold of the database. They define the structure of the database and the data that will be stored in it. They are also used to query the database. Since models are like classes, each sections and field that we create in the model card and datasheet are instances of the models with all the attributes.

Views
-----

Views can be found in the `views.py` file. The most important view is the `section` view which includes all the questions and fields. It handles post and get request and uses other views and functions in its logic. The other views usually redirects to the section view.
Every url in the `urls.py` file is connected to a view. The urls are used to access the views and the logic will not work without the urls. Whenever a new view is added, it should be added to the urls file as well.


The Logic of the Model Card
---------------------------

Once the questions are filled in the model card, the model card is ready the export it in several formats. At this point, the answers are stored in the database and by clicking, for example, html export, Django query the database and calls the main `create_model_card` function inside the `utils/model_card_lib_v2.py`. There the dataclass fields that is specified by the core library gets populated with the given answers. Then, populated model card fields are sent to jinja template to be rendered as static html. The function then returns to html file to be downloaded as attachment.   

The logic can be better understood with this diagram:

.. figure:: /_static/logic_backend.drawio.png
   :alt: Description of image for accessibility
   :align: center

   Model Card creation logic. 


The export formats are html, proto and json. The json format can be used to populate the fields in the web interface directly to make some modification or have a starting point.


The Logic of the Datasheet
--------------------------

For datasheet, a simpler approach is taken. The answers directly gets rendered into the html file and the html file is returned to the user to be downloaded as attachment.

Django Templates
----------------

Django templates are used to generate dynamic HTML content and are integral to the Django web framework. These templates allow for a clear separation between the presentation logic and business logic, aiding in the maintainability and readability of code.

Location
^^^^^^^^

By convention, the HTML files leveraging Django's templating engine are stored in the `templates` folder. This organization helps in keeping the structure clean and manageable. Depending on the complexity of the application, the `templates` folder can further contain sub-directories named after the respective Django apps, ensuring a modular structure.

Functionality
^^^^^^^^^^^^^

Django templates come with a built-in templating language that offers a wide array of tools:

- **Variables**: Display the value of Python expressions using double curly braces, like `{{ variable_name }}`.
  
- **Tags**: Execute certain logic such as loops and conditionals. For instance, `{% for item in items %}` ... `{% endfor %}` will loop through a list of items.
  
- **Filters**: Transform the values of variables and arguments. For example, `{{ name|lower }}` will display the name in lowercase.

Interaction with Views
^^^^^^^^^^^^^^^^^^^^^^

In a typical Django application, views fetch or compute data, then combine it with a template, and finally return an HttpResponse. This ensures a clear separation between data processing (view) and presentation (template). For instance, a view might fetch a list of articles from a database and then render these using an `articles.html` template.

URLs and Templates
^^^^^^^^^^^^^^^^^^

URL configurations in Django define URL patterns to match against the requested URL. Once matched, the associated view function is invoked. This view can then leverage a template to generate the final HTML response. Thus, the URL patterns indirectly determine which template gets displayed, based on the associated view's logic.

Power of Django Templates
^^^^^^^^^^^^^^^^^^^^^^^^^

Django templates are designed to be easy for non-programmers to read and write. At the same time, they offer the power and flexibility to cater to complex scenarios:

1. **Inheritance**: Templates can extend other templates using the `{% extends %}` tag. This promotes code reusability by allowing base templates to define structures and blocks that child templates can override.

2. **Includes**: Smaller reusable templates can be included in larger templates using the `{% include %}` tag, promoting modularity.

3. **Custom Tags and Filters**: While Django provides many built-in tags and filters, developers can also create custom ones tailored to specific needs.

4. **Safe Rendering**: Django templates escape content by default, offering protection against cross-site scripting (XSS) attacks.

5. **Context Processors**: These allow developers to make certain data available globally to all templates, ensuring common data is easily accessible.

Conclusion
----------

Django, with its MVT architectural pattern, has proven to be an invaluable framework for our project, seamlessly blending the data, logic, and presentation layers. From our models that effortlessly map to the database schema, to the views that process user requests, and the powerful templating system, each component plays a pivotal role in making our application both dynamic and scalable.

The models in our `mc_and_datasheet` app act as a foundation, ensuring data integrity and offering utilities to interact with the stored information. The views, residing in the heart of our application, are the gateways through which user interactions are managed, making use of both models and templates. And speaking of templates, their sheer flexibility, power, and security features like automatic data escaping demonstrate why Django is favored for web development.

Moreover, the integrated nature of Django means that adding new functionalities or making changes becomes significantly streamlined. The URL routing connects users to the right views, which in turn fetch or update data through models, and combine this data with templates to present the desired content. The logic of both our Model Card and Datasheet functionalities further showcases the adaptability and efficiency of Django's components.

In summary, this documentation elucidates the inner workings and the structure of our Django backend. As we continue to evolve our project, the principles and patterns detailed here will serve as guiding lights, ensuring we maintain clarity, efficiency, and maintainability in our codebase. For developers, both seasoned and new, we hope this provides a clear roadmap to understand and further enhance the functionalities of our application.
