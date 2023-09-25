Database Overview
=================

SQLite3 offers a lightweight, single-file database solution that's both portable and easy to manage. The database is encapsulated within a `db.sqlite3` file found in the main directory. This file has been compressed but can be decompressed to explore its contents.

To interact with this database, you have several recommended methods:

1. **SQLite3 Client**: While several SQLite3 clients are available, one particularly recommended client is `SQLiteBrowser <https://sqlitebrowser.org/>`_. Advanced users may prefer this direct method, but proceed with caution as it requires familiarity with SQL.

2. **Django ORM (Object Relational Mapping)**: Django's ORM provides an intuitive Python API for database interactions, allowing for complex queries and data manipulations.

3. **Django Admin Interface**: This is a built-in web interface from Django that facilitates direct CRUD operations on database records.

Django ORM Interaction
----------------------

Django's ORM is powerful and abstracts much of the complexity of database interactions. For a comprehensive understanding and tutorials on using the Django ORM, refer to the `official Django documentation <https://docs.djangoproject.com/en/stable/topics/db/models/>`_.

To harness the power of Django ORM:

- Enter the Django Shell:

  .. code-block:: bash

     python manage.py shell

  Once inside the shell, you can start querying and modifying the database using the ORM.

Django Admin Interface Usage
----------------------------

Django's Admin Interface is a dynamic web interface tailored for both developers and administrators. It simplifies many database operations without the need for additional code.

**Setting Up & Accessing**:

- Create a Superuser: Before accessing the admin interface, you need a superuser account.

  .. code-block:: bash

     python manage.py createsuperuser

  Follow the prompts to set up your superuser credentials.

- Login to the Admin Interface: Navigate to `http://localhost:8000/admin/` in your browser and log in with the credentials.

**Admin Interface Features**:

- Modifying Attributes: Adjust various attributes such as field descriptions, helper text, and more.
- Sessions Overview: View current active sessions and their associated data.
- Manage Sections & Fields: Add new sections and fields. Remember, additional logic might be needed if corresponding data classes in the core library are absent.

Conclusion
----------

Whether using the Django ORM or the Admin Interface, ensure a methodical and informed approach to maintain data integrity and seamless operations.
