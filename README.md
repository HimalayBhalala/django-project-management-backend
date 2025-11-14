# django-project-management-backend
Develop a Project Management System that helps to manage the tasks.

Note: This project is working totally using Python,so first check Python is installed or not inside your system.
First open the linux terminal and run the below command:
    Command: python3 --version  (getting output like -> Python 3.12.3 (version may be different)) 
Above format is not shown while entering above command that means python is not installed, then install it using the below command:
    Command: sudo apt install python3

# Project Overview
Project Management System is used to manage users and their tasks within a created project. It allows users to create and manage tasks, communicate through task comments, and also getting the status of assigned tasks such as pending, in_progress and completed.

# Follow Below Steps to Work with Project Management System(Run Project Locally)
# Step 1:
-> First check Git is installed or not in the system.
    Command: git --version

-> If Git is installed, output will be like:
git version 2.39.1 (version may be different)

-> If Git is not installed, install it using the below command:
    Command: sudo apt install git -y  (here -y flag is used to install all the Git dependencies)

-> After GitHub is available, clone the GitHub repository for getting the updated code.
    Command: git clone github_repository_url

-> Once project is clone so include a .env file and also set a require secrets for run a Project.

# Step 2:
-> After cloning the repository, first create a virtual environment because it gives a separate environment for our project.

-> Drawback of not using virtual environment:
For example: Project1 (old_project) is working with another DRF version and Project2 (latest_project) uses the updated version of DRF. This will create a conflict version issue. To resolve that, we use virtual environment.

-> Create virtual environment in linux:
    Command: python3 -m venv virtual_env_name  (here we use python3 because version is 3.12.3 (version may be diffrent))

-> Activate virtual environment:
    Command: source virtual_env_name/bin/activate

-> After activating virtual environment, install required dependencies using pip.
For example, install Django:
    Command: pip install django

-> If you want to install dependencies from requirements.txt file:
    Command: pip install -r requirements.txt (here -r flag is used to read all the dependencies included inside requirements.txt)

-> To confirm which dependencies are installed:
    Command: pip list

-> If everything is right based on above instruction so include .env file from the root folder.
    =>  - accounts
        - project_management
        - projects
        - virtual_env_name
        - .env

-> Use below command for migrations first (here migration is used to keep creating and updating model information),
    Command: python3 manage.py makemigrations

-> For apply those migrations change in database so used below commnad,
    Command: python3 manage.py migrate

-> If above command run successfully after that run the django server using,
    Command: python3 manage.py runserver

    -> Project start successfully so getting below message like,
        Django version 5.2.8, using settings 'project_management.settings'
        Starting development server at http://127.0.0.1:8000/

-> Server is started so open a postman and import a api collection and envionment collection first and use below api

# Project APIs
1) accounts app folder: This folder include all of user related apis like register new user, login user, show user profile, update user profile.

    base_path = "http://127.0.0.1:8000/apis/accounts/
    1) Registration :
        API(POST Method) => base_path/register/
    2) Login: 
        API(POST Method) => base_path/login/
    3) Get User Profile:
        API(GET Method)  => base_path/me/
    4) Update User Profile:
        API(PATCH Method)=> base_path/me/

2) projects app folder: Helpfull for getting all list of project, creating a new project, getting a project detail, update it's fully detail or partial detail, delete the project if not needed, able to assign new member inside the project and also able to mark as a completed project.

    base_path = "http://127.0.0.1:8000/apis/projects/
    1) Get List Of Projects:
        API(GET Method)   => base_path
    2) Create Project:
        API(POST Method)  => base_path
    3) Get Project Detail:
        API(GET Method)   => base_path/<project_id>/
    4) Update Project:
        API(PUT Method)   => base_path/<project_id>/
    5) Partially Update Project:
        API(PATCH Method) => base_path/<project_id>/
    6) Delete Project:
        API(DELETE Method)=> base_path/<project_id>/
    7) Assigned Member:
        API(POST Method)  => base_path/<project_id>/add-member/
    8) Mark Project Completed:
        API(POST Method)  => base_path/<project_id>/complete/