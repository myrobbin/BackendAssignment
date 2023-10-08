#  BackendAssignment Project README

This is a Django project with the following setup:

- **Virtual Environment**: 
  - Must have`virtualenv` installed. If not, install it with: `virtualenv myenv -p python3`
  - I have use python 3.10 version for this project
  - Create a new virtual environment:
    ```
    virtualenv myenv -p python3
    ```
  - Activate the environment ( use `source myenv/bin/activate`):
    ```
    source myenv/bin/activate
    ```

- **Requirements.txt**:
  - Install project dependencies using the requirements.txt file:
    ```
    pip install -r requirements.txt
    ```

- **drf-yasg for Swagger**:
  - [drf-yasg](https://github.com/axnsan12/drf-yasg) is used for Swagger documentation.

## Setup Instructions

1. **Virtual Environment**:

    ```bash
    virtualenv myenv -p python3
    source myenv/bin/activate  # Use this command to activate the environment.
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
   
3. **Create .env File**:
   - Create a `.env` file in the root directory of your project.
   - Add your configuration parameters in the `.env` file.

4. **Run the Application**:

    ```bash
    python manage.py runserver
    ```

5. **Access Swagger Documentation**:

   Once the server is running, navigate to `http://127.0.0.1:8000/swagger/` to access the Swagger documentation.


