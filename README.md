# robot_interface
A FastAPI project to instruct a robot on the moon.

This is a project that used `PostgreSQL` database.

## Installation Guide

How to set up the project using `PostgreSQL` and `python3.10`:

1.  Now, we can begin setting up our project. First, create a virtual environment and active that:

        python3.10 -m venv venv

        source venv/bin/activate

2.  Now you can install the project requirements one by one using `pip install` or using:

        pip install -r requirements.txt

3.  To use `PostgreSQL` we need to install it:

        sudo apt-get install postgresql

    - Now we need to switch to the newly created postgresql user to create a database user and a database:

          	sudo -i -u postgres
          	createuser --interactive --pwprompt

    - Enter unique name to database user and password

      createdb YOUR_DB_NAME

    - now update the configs.py file in this project and change `sqlalchemy_string`


## Getting Started

After requirement installation and creating `PostgreSQL` database (that described in installation guide), Run this project with this command and open http://127.0.0.1:8000/docs with your browser to see the result:

	uvicorn app.main:app

