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

        Input: {
                    "email": "rajesh@gmail.com",
                    "password": "Rajesh@12345"
               }

        Output: {
                    "status": "success",
                    "message": "Registration success",
                    "data": {
                        "first_name": "",
                        "last_name": "",
                        "username": "rajesh",
                        "email": "rajesh@gmail.com",
                        "phone": "",
                        "dob": null
                    }
                }
    2) Login: 
        API(POST Method) => base_path/login/

        Input : {
                    "email": "rajesh@gmail.com",
                    "password": "Rajesh@12345"
                }

        Output : {
                    "status": "success",
                    "message": "Login success",
                    "data": {
                        "user": {
                            "first_name": "",
                            "last_name": "",
                            "username": "rajesh",
                            "email": "rajesh@gmail.com",
                            "phone": "",
                            "dob": null
                        },
                        "token": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhIjgifQ.mqDBErxOCRjQRLdvX1RSQDvzMdz6dxG6EwPcMG0-SOY",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlI-7G9PM6itsM8c3UX1fME"
                        }
                    }
                }

        NOTE: Copy access_token and past it inside the postman environment

    3) Get User Profile:
        API(GET Method)  => base_path/me/
                    
        Output : {
                    "status": "success",
                    "message": "Profile getting successfully",
                    "data": {
                        "first_name": "",
                        "last_name": "",
                        "username": "rajesh",
                        "email": "rajesh@gmail.com",
                        "phone": "",
                        "dob": null
                    }
                }
    4) Update User Profile:
        API(PATCH Method)=> base_path/me/

        Input : {
                    "first_name" : "Rajesh",
                    "last_name" : "Pathak"
                }

        Output : {
                    "status": "success",
                    "message": "Profile updated successfully",
                    "data": {
                        "first_name": "Rajesh",
                        "last_name": "Pathak",
                        "username": "Rajesh Pathak",
                        "email": "rajesh@gmail.com",
                        "phone": "",
                        "dob": null
                    }
                }


2) projects app folder: Helpfull for getting all list of project, creating a new project, getting a project detail, update it's fully detail or partial detail, delete the project if not needed, able to assign new member inside the project and also able to mark as a completed project.

    base_path = "http://127.0.0.1:8000/apis/projects/
    1) Get List Of Projects:
        API(GET Method)   => base_path

        Output : {
                    "status": "success",
                    "message": "Projects fetched successfully",
                    "next": null,
                    "previous": null,
                    "data": [
                        {
                            "id": 17,
                            "name": "MakeMyTrip",
                            "description": "",
                            "created_by": {
                                "username": "Rajesh Pathak",
                                "email": "rajesh@gmail.com"
                            },
                            "status": "active"
                        }
                    ]
                }
    2) Create Project:
        API(POST Method)  => base_path

        Input : {
                    "name": "Youtube"
                }

        Output: {
                    "status": "success",
                    "message": "Projects created successfully",
                    "data": {
                        "id": 18,
                        "name": "YouTube",
                        "description": "",
                        "created_by": {
                            "username": "Rajesh Pathak",
                            "email": "rajesh@gmail.com"
                        },
                        "status": "active"
                    }
                }

    3) Get Project Detail:
        API(GET Method)   => base_path/<project_id>/

        Output : {
                    "status": "success",
                    "message": "Project retrieve successfully",
                    "data": {
                        "id": 15,
                        "name": "Youtube",
                        "description": "",
                        "members": [
                            {
                                "username": "Rajesh Pathak",
                                "email": "rajesh@gmail.com"
                            }
                        ],
                        "status": "active",
                        "created_at": "2025-11-16T09:16:37.796961Z"
                    }
                }
    4) Update Project:
        API(PUT Method)   => base_path/<project_id>/

        Input : {
                    "name": "Rail MakemyTripe",
                    "description": "This project is help us getting all train related information",
                    "status": "completed"
                }

        Output: {
                    "status": "success",
                    "message": "Project updated successfully",
                    "data": {
                        "id": 17,
                        "name": "Rail MakemyTripe",
                        "description": "This project is help us getting all train related information",
                        "created_by": {
                            "username": "Rajesh Pathak",
                            "email": "rajesh@gmail.com"
                        },
                        "status": "completed"
                    }
                }
    5) Partially Update Project:
        API(PATCH Method) => base_path/<project_id>/

        Input : {
                    "status":"archived"
                }

        Output: {
                    "status": "success",
                    "message": "Project updated successfully",
                    "data": {
                        "id": 17,
                        "name": "Rail MakemyTripe",
                        "description": "This project is help us getting all train related information",
                        "created_by": {
                            "username": "Rajesh Pathak",
                            "email": "rajesh@gmail.com"
                        },
                        "status": "archived"
                    }
                }
    6) Delete Project:
        API(DELETE Method)=> base_path/<project_id>/

        Output: {
                    "status": "success",
                    "message": "Project remove successfully",
                    "data": []
                }
    7) Assigned Member:
        API(POST Method)  => base_path/<project_id>/add-member/

        Input: {
                    "members": [7]
                }

        Output: {
                    "status": "success",
                    "message": "Assign member successfully for Rail MakemyTripe",
                    "data": {
                        "id": 17,
                        "name": "Rail MakemyTripe",
                        "description": "This project is help us getting all train related information",
                        "created_by": "Rajesh Pathak",
                        "members": [
                            {
                                "username": "admin",
                                "email": "admin@gmail.com"
                            },
                            {
                                "username": "Rajesh Pathak",
                                "email": "rajesh@gmail.com"
                            }
                        ],
                        "status": "archived",
                        "created_at": "2025-11-16T09:25:48.776967Z"
                    }
                }
    8) Mark Project Completed:
        API(POST Method)  => base_path/<project_id>/complete/

        Output: {
                    "status": "success",
                    "message": "Project completed successfully",
                    "data": {
                        "id": 17,
                        "name": "Rail MakemyTripe",
                        "description": "This project is help us getting all train related information",
                        "created_by": "Rajesh Pathak",
                        "members": [
                            {
                                "username": "admin",
                                "email": "admin@gmail.com"
                            },
                            {
                                "username": "Rajesh Pathak",
                                "email": "rajesh@gmail.com"
                            }
                        ],
                        "status": "completed",
                        "created_at": "2025-11-16T09:25:48.776967Z"
                    }
                }


3) tasks app folder: Helpfull for getting the project related all the tasks, create a new task for a project, get a detail of an task, fully updated the task information, partial update the task, delete a task, gettign all task releted comments, create a new comment based on task and also filter the comments data functionality
    
    base_path = "http://127.0.0.1:8000/apis/tasks/

    1) Get List Of Tasks:
        API(GET Method)    => base_path or base_path/?page=<page_number> (using pagination)

        Output: {
                    "status": "success",
                    "message": "Tasks getting successfully",
                    "next": null,
                    "previous": null,
                    "data": []
                }
    2) Create Task:
        API(POST Method)   => base_path

        Input: {
                    "title": "Backend",
                    "description": "Completed Backend authenticationa and authorization the pages for Project Management System",
                    "project": "17"
                }

        Output: {
                    "status": "success",
                    "message": "Task created successfully",
                    "data": {
                        "id": 14,
                        "title": "Backend",
                        "description": "Completed Backend authenticationa and authorization the pages for Project Management System",
                        "project": 17,
                        "status": "pending",
                        "due_date": null
                    }
                }
    3) Get Task  Detail:
        API(GET Method)    => base_path/<task_id>/

        Output: {
                    "status": "success",
                    "message": "task retrieve successfully",
                    "data": {
                        "id": 14,
                        "title": "Backend",
                        "description": "Completed Backend authenticationa and authorization the pages for Project Management System",
                        "project": 17,
                        "assigned_to": null,
                        "status": "pending",
                        "due_date": null,
                        "created_at": "2025-11-16T09:58:58.008141Z",
                        "comments": []
                    }
                }
    4) Update Task:
        API(PUT Method)    => base_path/<task_id>/

        Input: {
                    "title": "UI/UX",
                    "description": "Completed design section",
                    "project": "17",
                    "due_date": "2025-11-15"
                }

        Output: {
                    "status": "success",
                    "message": "Task modify successfully",
                    "data": {
                        "id": 14,
                        "title": "UI/UX",
                        "description": "Completed design section",
                        "project": 17,
                        "status": "pending",
                        "due_date": "2025-11-15"
                    }
                }
    5) Partially Update Task:
        API(PATCH Method)  => base_path/<task_id>/

        Input: {
                    "status":"in_progress"
                }

        Output: {
                    "status": "success",
                    "message": "Task modify successfully",
                    "data": {
                        "id": 14,
                        "title": "UI/UX",
                        "description": "Completed design section",
                        "project": 17,
                        "status": "in_progress",
                        "due_date": "2025-11-15"
                    }
                }
    6) Delete Task:
        API(DELETE Method) => base_path/<task_id>/

        Output: {
                    "status": "success",
                    "message": "Task remove successfully",
                    "data": []
                }
    7) Assign Task:
        API(POST Method)   => base_path/<task_id>/assign/

        Input : {
                    "assigned_to": 7
                }

        Output : {
                    "status": "success",
                    "message": "Task assigned successfully",
                    "data": {
                        "id": 14,
                        "title": "UI/UX",
                        "description": "Completed design section",
                        "project": 17,
                        "assigned_to": 7,
                        "status": "in_progress",
                        "due_date": "2025-11-15",
                        "created_at": "2025-11-16T09:58:58.008141Z",
                        "comments": []
                    }
                }
    8) Mark as a Complete:
        API(POST Method)   => base_path/<task_id>/complete/

        Output: {
                    "status": "success",
                    "message": "Task completed successfully",
                    "data": {
                        "id": 14,
                        "title": "UI/UX",
                        "description": "Completed design section",
                        "project": 17,
                        "assigned_to": 7,
                        "status": "completed",
                        "due_date": "2025-11-15",
                        "created_at": "2025-11-16T09:58:58.008141Z",
                        "comments": []
                    }
                }
    9) Get All Task Related Comment:
        API(GET Method)    => base_path/<task_id>/comments/

        Output: {
                    "status": "success",
                    "message": "Comment retrieve successfully",
                    "data": []
                }
    10) Include a New Comment:
        API(POST Method)   => base_path/<task_id>/comments/

        Input: {
                    "text": "Please completed design section as soon as possible"
                }

        Output: {
                    "status": "success",
                    "message": "Comment added successfully",
                    "data": {
                        "id": 1,
                        "task": 14,
                        "author": 8,
                        "text": "Please completed design section as soon as possible",
                        "created_at": "2025-11-16T10:08:54.623608Z"
                    }
                }

    For Gettig All Comments:

        base_path = "http://127.0.0.1:8000/apis/comments/

        1) Get List Of Comments:
           API(GET Method) => base_path

           Output: {
                        "count": 1,
                        "next": null,
                        "previous": null,
                        "results": [
                            {
                                "id": 1,
                                "project": 17,
                                "task": {
                                    "id": 14,
                                    "title": "UI/UX",
                                    "description": "Completed design section",
                                    "project": 17,
                                    "assigned_to": 7,
                                    "status": "completed",
                                    "due_date": "2025-11-15",
                                    "created_at": "2025-11-16T09:58:58.008141Z"
                                },
                                "text": "Please completed design section as soon as possible",
                                "author": 8,
                                "created_at": "2025-11-16T10:08:54.623608Z"
                            }
                        ]
                    }