Tests
=====

Testing Importance
------------------

Testing is a crucial component in the development of software applications. It allows developers to ensure that each part of their application works as intended. The primary benefits and importance of testing include:

- **Quality Assurance:** Testing helps in identifying and fixing bugs and errors, ensuring that the final product works smoothly and efficiently.
- **Improved Performance:** Consistent testing leads to enhanced performance of the application, providing a better user experience.
- **Cost-Efficiency:** Identifying and addressing issues early in the development process can save time and resources in the long run.
- **Security:** Through testing, developers can identify and mitigate security vulnerabilities in the application, protecting users and data.
- **Customer Satisfaction:** A well-tested application is likely to be more reliable and user-friendly, leading to increased customer satisfaction.

GitHub Actions and Testing
--------------------------

GitHub Actions automates the testing process by triggering a series of commands (defined in a workflow file) upon specific GitHub events, such as pushing a commit or opening a pull request. This automation allows for:

- **Continuous Integration (CI):** Automatically building and testing your code in multiple environments to ensure it works as expected.
- **Continuous Deployment (CD):** Automatically deploying your application once it passes all tests, streamlining the release process.
- **Feedback Loop:** Providing immediate feedback on the success or failure of tests, making it easier for developers to identify and fix issues.

Containerization with GitHub Actions
------------------------------------

Containerization involves packaging an application and its dependencies together in a container. With GitHub Actions, you can automatically build and push Docker images when certain events occur, further automating the deployment process. While containerization is valuable for ensuring consistency across multiple environments and simplifying deployment, it is not mandatory for every project. The decision to use containerization depends on the specific needs and context of the application being developed. At the current stage, the app is not being deployed from the docker container but directly from the django folder.

Implemented Tests
-----------------

Tests can be found in `mc_and_datasheet/tests.py`. 

- **test_model_card_creation:** Tests that whether model card can be created from the mock input.
- **test_section_view_get_request:** Tests whether section view get the request and renders the template.
- **test_with_session:** Tests that whether the adding section and new fields work.
- **test_createoutput:** Creates a mock datacard entry and files and tests whether the inputs of the `create_model_card` are not empty.


.. note::

        Implemented tests are not enough to cover all the functionalities of the app. They are testing only the basic functions of the app. More tests should be implemented to cover the server-side functionalities of the app. As the bugs are fixed and improvements made, more tests should be implemented to cover the new functionalities.


