Views
=====

In this page, the overview of the functions that are used in `views.py` is provided. There are view functions named 
- impressum
- legal
- about
- contact
- datacard_section

These functions have only one purpose: to render the corresponding HTML template. The other long view functions are listed in the order they appear in the file.

home
====
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles requests directed to the home page of the application.
- Ensures the creation and retrieval of a session identifier (`session_uuid`), which is stored in the user's session. This session identifier is not directly used but has potential uses in the future.
- Retrieves and prints the Django `session_key` for the user's session.
- Renders and returns the `home.html` template.

Parameters
^^^^^^^^^^
- `request`: The HTTP request object received from the client.

Return Value
^^^^^^^^^^^^
- Renders and returns the `home.html` template.


get_session_id
==============
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Retrieves the user's session key from the received request object.
- Queries the Django `Session` model to get the session object associated with the user's session key.
- Retrieves and returns the `session_key` from the session object.

Parameters
^^^^^^^^^^
- `request`: The HTTP request object received from the client.

Return Value
------------
- Returns the `session_key` associated with the user's session.

upload_file
===========
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles file upload requests from the client.
- Retrieves the session key and queries the database to get the section instance and section list.
- If the request method is `POST` and the form is valid, it creates a `File` instance, saves the uploaded file to the specified path, and saves the `File` instance to the database.
- Redirects the client to a specific URL using `HttpResponseRedirect`.

Parameters
^^^^^^^^^^
- `response`: The HTTP response object.
- `id`: The identifier of a section.

Return Value
^^^^^^^^^^^^
- Redirects to a specific URL after processing the uploaded file and renders the `section.html` template.

upload_json
===========
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles JSON file upload requests.
- Retrieves the session key and processes the uploaded JSON file if present in the request.
- This function is triggered when user wants to populate the fields with the json_file directly.
- Redirects the client to a specific URL using `HttpResponseRedirect`.

Parameters
^^^^^^^^^^
- `response`: The HTTP response object.
- `id`: Identifier (not used in the function but passed as a parameter).

Return Value
^^^^^^^^^^^^
- Redirects to a specific URL after processing the uploaded JSON file to the `section` view.

delete
======
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles data deletion requests.
- It deletes various data objects and files based on the session key and other conditions.
- The function is triggered from the user interface when the user clicks on the delete button.
- Redirects the client to a specific URL using `HttpResponseRedirect`.

Parameters
^^^^^^^^^^
- `response`: The HTTP response object.
- `id`: Identifier (not used in the function but passed as a parameter).

Return Value
^^^^^^^^^^^^
- Redirects to the `section` view after performing deletion operations .

section
=======
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles requests directed to specific sections.
- Retrieves the session key and uses it to query and get the section instance and associated data from the database.
- This view is responsible to render all the sections of the model card and. It has logics for saving, deleting, adding fields and sections.

Parameters
^^^^^^^^^^
- `response`: The HTTP response object.
- `id`: The identifier of a section.

Return Value
^^^^^^^^^^^^
- Renders and returns the `section.html` template with the provided context.

retrievedata
============
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Processes and structures data related to sections for further usage.
- Retrieves and organizes section data into a dictionary, then converts it into a JSON string.
- Interacts with the `CardSectionData` model to get or create data entries.
- Prints messages indicating whether a new instance was created or an existing one was updated.

Parameters
^^^^^^^^^^
- `section_name`: The name of a section.
- `field_questions`: Questions associated with the fields in a section.
- `field_answers`: Answers associated with the fields in a section.

Return Value
^^^^^^^^^^^^
- Returns a variable called T which is a json string to be used to save the data to database.

createoutput
============
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles requests for creating output based on the user's session and selected format.
- Retrieves session key and interacts with the `CardData` model to get the most recent entry.
- Processes and structures the retrieved data, then interacts with `File` objects.

Parameters
^^^^^^^^^^
- `request`: The HTTP request object received from the client.
- `id`: Identifier associated with the request.

Return Value
^^^^^^^^^^^^
- (To be analyzed and documented further.)

datasheet_export
================
Purpose/Description
^^^^^^^^^^^^^^^^^^^
- Handles requests for exporting datasheets.
- Interacts with the `CardDataDatasheet` model to get the most recent entry and processes the retrieved data.
- Creates an `HttpResponse` object with the processed data and prompts the user to save the file.

Parameters
^^^^^^^^^^
- `request`: The HTTP request object received from the client.
- `id`: Identifier associated with the request.

Return Value
^^^^^^^^^^^^
- An `HttpResponse` object with the processed data and a prompt for the user to save the file.
