#  Introduction
## API Endpoints (url / uri)
 CRUD : Create, Retrieve, Update, Delete 
 Create List and Search
## HTTP methods (client side)
GET, POST, PUT, MATCH, DELETE    
## Data Types and Validation
Use a serializer for consistency 
JSON -> Serializer
Validation -> Serializer
## References
If you get stuck during the development of your project you can contact me on Github
## Project prompt
The application will allow a user to post a project he/she has created and get it reviewed by his/her peers.
A project can be rated based on 3 different criteria

* Design
* Usability
* Content
* These criteria can be reviewed on a scale of 1-10 and the average score is taken.

## User stories
As a user, you can:

View posted projects and their details.
* Post a project to be rated/reviewed
* Rate/ review other users' projects
* Search for projects 
* View projects overall score
* View my profile page.
* [live site](https://awaaa.herokuapp.com/)

## API Endpoints
Users can access data from this application via an API.There are two API endpoints:
* Profile - This endpoint should return all the user profiles with information such as the username, bio, projects of the user and profile picture 
* Projects- This endpoint should return information pertaining to all the projects posted in your application.

## Getting Started.
These instructions will get you a copy of the project up and running on a local host.

Step 1: git clone
<br />Step 2: Enter the Project root folder

cd gallery/
<br />install virtual environment (venv) without pip

python3.6 -m venv --without-pip virtual
<br />Step 3: Activate virtual environment

<br />source virtual/bin/activate.
<br />install pip using curl.
## Built With
* Python3.6 - Python is a programming language that lets you work quickly and integrate systems more effectively.
* Django - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* postgresql - PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
## Bugs
If you encounter any bugs, email me on leskeylevy@gmail.com. If you would like to add some changes, please feel free to
fork the project and make a pull request.

## Authors
LESKEYLEVY

## License
This project is licensed under the MIT License.

## Acknowledgments
Moringa School.
