HTML Structure
==============

Overview
--------
The app consists of 10 html files with `section.html` and `dt_section.html` being the most significant. Every html file extends the `base.html` except for `impresum.html` and `legal.html`. 
`base.html` incorporates the top navigation bar and the footer. `section.html` and `dt_section.html` function as the main pages, displaying sections and fields, complemented by a side navigation bar.

Static content, such as CSS, JS, and image files, resides within the `mc_and_datasheet` directory's static folder. While the HTML files leverage open-source JS and CSS codes, they also introduce specific CSS codes, which take precedence over others. Additionally, JavaScript is embedded directly within the HTML files to add functionalities.

To provide a clearer understanding of the intricacies of the HTML structure, let's delve deeper into the `section.html` file, which stands out due to its complexity.

Detailed Breakdown of section.html
----------------------------------

Template Structure and Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The `section.html` file is a Django template that extends from `mc_and_datasheet/base.html`:

.. code-block:: html

    {% extends 'mc_and_datasheet/base.html' %}

This indicates it inherits the foundational structure from `base.html` and can overwrite or append to specific blocks defined in the base template. The title of this page is determined as "Section" through the `{% block title %}`.

CSS Styles
^^^^^^^^^^
There are 7 CSS stylesheets linked in this file:

1. **Local Styles**:
    - Essential styles for jQuery UI components, Bootstrap specifics for the project, styles for the sidebar component, and distinct styles for the section are evident.

      .. code-block:: html

        <link rel="stylesheet" href="{% static 'mc_and_datasheet/css/jquery-ui.css' %}">

2. **External Styles**:
    - External styles, such as FontAwesome, Bootstrap, and Google Fonts, are utilized.

      .. code-block:: html

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />

JavaScript Functionality
^^^^^^^^^^^^^^^^^^^^^^^^
The template incorporates 24 JavaScript scripts, adding interactivity to the page:

.. code-block:: javascript

    document.querySelector('.drop-zone').ondragenter = function() {
        this.style.cursor = "pointer";
        ...
    }

Django Template Mechanics
^^^^^^^^^^^^^^^^^^^^^^^^^
Django's templating engine shines in this file:

- **For Loops**: Iterates over lists or querysets, enabling dynamic rendering.

  .. code-block:: html

    {% for section in section_list %}
         ...
    {% endfor %}

- **If Conditions**: Conditionally renders sections of the template.

  .. code-block:: html

    {% if section.id == current_section_id %}active{% endif %}

User Input and Forms
^^^^^^^^^^^^^^^^^^^^
Five forms are embedded in the template:

.. code-block:: html

    <form method="POST">
               ...
    </form>

Each form defines its method (typically "POST" or "GET") and an associated action, which is the URL the form data targets upon submission.

Conclusion
^^^^^^^^^^
The `section.html` file epitomizes a comprehensive Django template, melding static and dynamic content. It adeptly employs CSS for aesthetic appeal, JavaScript for interactivity, and Django's templating tags for dynamic content presentation, rendering it a pivotal element in the application's user interface.
