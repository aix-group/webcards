Sessions
========

Introduction to Django Sessions
-------------------------------
Django provides a session framework that allows you to store and retrieve arbitrary data on a per-site-visitor basis. It stores data on the server side and abstracts the sending and receiving of cookies. Sessions offer a way to remember users' (or visitors') data across multiple requests.

While authenticated sessions are tied to specific users, Django also supports anonymous sessions, which are not bound to users but can still hold data across multiple requests. This is useful for tracking visitor data without needing them to log in.

Using Django's Anonymous Sessions
---------------------------------
To utilize Django's session framework, it should be included in the `INSTALLED_APPS` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.sessions',
        ...
    ]

Next, you'll need to decide where you want to store session data. Django can store session data in various places: in databases, in cached files, or in memory. The default is to use database-backed sessions. To use database-backed sessions, you need to run:

.. code-block:: bash

    python manage.py migrate

This will create a table in your database named `django_session` where session data will be saved.

Application-Specific Implementation
-----------------------------------
In the application, we embrace a login-free approach and, as a result, heavily rely on anonymous sessions. Every time a user visits the webpage, a process is initiated that sends a session ID from the database to the browser's cookies. This session ID ensures that each user's data remains distinct and doesn't get entangled with the data of others. The application uses Django sessions primarily to store the uploaded JSON model card data. While Django sessions offer a vast array of uses, in this specific application, the primary use case revolves around maintaining user-specific data tied to their session ID. The session ID acts as a unique identifier, ensuring that users' data doesn't mix up with others.

Data affiliated with a user is tied to their session ID. This is achieved by appending a `_session_id` suffix to various class variables. When creating or querying data, it's filtered using this session ID, ensuring data integrity for each user.

The session cookie age has been set to persist for 30 days:

.. code-block:: python

    SESSION_COOKIE_AGE = 30 * 24 * 60 * 60

However, after session id is expired, it just becomes inactive and user data might still be in the database. For that reason, a cleanup mechanism has been implemented.

Cleaning User Data
------------------
To ensure that stale and expired session data doesn't accumulate, an app named `cleanup_sessions` was developed. This app contains a management command that:

1. Identifies active sessions from the database.
2. Removes temporary `CardSectionData`.
3. Cleans the 'model_card_json' from the session.
4. Deletes specific sections and fields tied to a session ID.
5. Resets specific field values and counters.
6. Cleans up files and directories related to a session.
7. Flushes the session to ensure all session data is removed.

.. code-block:: bash

    python manage.py cleanup_sessions

This cleanup procedure can be triggered manually or scheduled periodically using tools like cron on a Linux-based system.

Conclusion
----------
Django's session framework is powerful and versatile. In this application, it's been tailored to manage user-specific data without requiring authentication, using a unique session ID strategy. A cleanup mechanism further ensures data hygiene and optimal database performance.
