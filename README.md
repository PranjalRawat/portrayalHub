# PortrayalHub

### Central hub for portraying your skills and projects

---

Make sure you have the latest version of python installed: https://www.python.org/downloads/

## Build Instructions

-   Check the minimum supported python version in [Pipfile](Pipfile)(`python_version` property). Current supported minimum version is `3.9`.
-   Using [pip](https://pypi.org/project/pipenv/) for package management, install pipenv `pip install pipenv`
-   (Optional) If you have multiple python versions installed, install it using `pip3 install pipenv`
-   Navigate to project root dir and Run `pipenv shell` to create a virtual env
-   Run `pipenv install` to install all required packages
-   Run `python3 manage.py runserver` for starting a lightweight development server
-   Open 'https://127.0.0.1:8000/api/' in browser for web view

    ![portrayalHub](/portrayalHub/medias/portrayalHub_API_dashboard.png)

## Testing Application

1. Open Command-Line in the project root directory
2. Run the virtual environment
3. **Testing models** - Executing models tests
    - Run `python3 manage.py test portfolioApi.tests.models`
4. **Testing views** - Executing views tests
    - Run `python3 manage.py test portfolioApi.tests.views`

## Project SwaggerUI API view

Once an application is running, you can access the SwaggerUI API view by following these steps:

1. Go to <https://127.0.0.1:8000/api/docs>
2. All the URL and Views are visible.

    - ### For Authenticated users:

        - **Profile :** <http://127.0.0.1:8000/api/docs/#/profile>
          ![Profile swaggerUI](/portrayalHub/medias/profile_swaggerUI.png)

        - **Social Platforms :** <http://127.0.0.1:8000/api/docs/#/social_platforms>
          ![Social Platforms swaggerUI](/portrayalHub/medias/socialPlatforms_swaggerUI.png)

        - **Educations :** <http://127.0.0.1:8000/api/docs/#/education>
          ![Education swaggerUI](/portrayalHub/medias/education_swaggerUI.png)

        - **Skills :** <http://127.0.0.1:8000/api/docs/#/skills>
          ![Skills swaggerUI](/portrayalHub/medias/skills_swaggerUI.png)

        - **Experience :** <http://127.0.0.1:8000/api/docs/#/experience>
          ![Experience swaggerUI](/portrayalHub/medias/experience_swaggerUI.png)

        - **Projects :** <http://127.0.0.1:8000/api/docs/#/projects>
          ![Projects swaggerUI](/portrayalHub/medias/projects_swaggerUI.png)

        - **Certificate :** <http://127.0.0.1:8000/api/docs/#/certificates>
          ![Certificate swaggerUI](/portrayalHub/medias/certificate_swaggerUI.png)

    - ### For Un-Authenticated users:

        - **Users :** <http://127.0.0.1:8000/api/docs/#/user>
          ![Users swaggerUI](/portrayalHub/medias/usets_swaggerUI.png)
