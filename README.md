# CodeCraftHub

CodeCraftHub is a beginner-friendly personalized learning platform API built with Python and Flask.

The application allows developers to keep track of courses they want to learn. Each course includes a name, description, target completion date, current learning status, automatically generated ID, and creation timestamp.

Course data is stored in a simple `courses.json` file, so no database setup is required.

---

## Project Overview

CodeCraftHub provides a REST API for managing learning courses.

You can use the API to:

- Create a new course
- View all courses
- View one course
- Update an existing course
- Delete a course
- Store course data permanently in a JSON file

This project is designed to help beginners learn the basics of:

- Python programming
- Flask
- REST API design
- HTTP methods
- JSON request and response data
- Input validation
- File-based data persistence

---

## Project Objectives

The objectives of CodeCraftHub are to:

1. Build a simple REST API using Flask.
2. Practice creating CRUD operations.
3. Store application data in a JSON file.
4. Validate incoming request data.
5. Return useful HTTP status codes.
6. Handle common errors clearly.
7. Create a beginner-friendly backend project.

CRUD means:

|
 Operation 
|
 Meaning 
|
 HTTP method 
|
|
---
|
---
|
---
|
|
 Create 
|
 Add a new course 
|
`POST`
|
|
 Read 
|
 View courses 
|
`GET`
|
|
 Update 
|
 Change a course 
|
`PUT`
|
|
 Delete 
|
 Remove a course 
|
`DELETE`
|

---

## Features

CodeCraftHub includes the following features:

- Create courses
- View all courses
- View one course by ID
- Update courses
- Delete courses
- Automatically generated integer IDs
- IDs start from `1`
- Unique course IDs
- Automatically generated `created_at` timestamps
- Course status validation
- Target date validation
- Required field validation
- Empty field validation
- Invalid JSON handling
- Invalid course ID handling
- Course-not-found handling
- Automatic creation of `courses.json`
- Persistent data storage between application restarts
- JSON responses for successful and unsuccessful requests

---

## Technologies Used

The project uses:

- Python
- Flask
- JSON
- REST API
- `curl` for optional API testing

No external database is required.

---

## Project Structure

A simple CodeCraftHub project can have the following structure:

```text
codecrafthub/
├── app.py
├── courses.json
├── requirements.txt
└── README.md
app.py
Contains:

The Flask application
API routes
Course validation
JSON file reading
JSON file writing
Error handling
courses.json
Stores all course data.

The file is created automatically when the application starts if it does not already exist.

requirements.txt
Contains the Python packages required by the project.

Example:

Flask
README.md
Contains project documentation and instructions.

Prerequisites
Before running CodeCraftHub, install the following:

Python 3.8 or newer
A terminal application
A text editor or code editor
To check whether Python is installed, open a terminal and run:

python --version
On some systems, you may need to use:

python3 --version
You should see a version similar to:

Python 3.12.0
Installation
Step 1: Create the project folder
Create a folder named
codecrafthub
.

On Windows Command Prompt:

mkdir codecrafthub
cd codecrafthub
On Windows PowerShell:

New-Item -ItemType Directory codecrafthub
Set-Location codecrafthub
On macOS or Linux:

mkdir codecrafthub
cd codecrafthub
Step 2: Add the project files
Place the following files in the project folder:

app.py
requirements.txt
README.md
You do not need to create
courses.json
manually. The application creates it automatically if it does not exist.

Creating a Python Virtual Environment
A virtual environment keeps the project's Python packages separate from other Python projects.

Windows Command Prompt
From inside the project folder, run:

python -m venv venv
Activate the virtual environment:

venv\Scripts\activate
After activation, the terminal usually shows
(venv)
at the beginning of the command line.

Example:

(venv) C:\path\to\codecrafthub>
Windows PowerShell
Create the virtual environment:

python -m venv venv
Activate it:

.\venv\Scripts\Activate.ps1
If PowerShell prevents the activation script from running, open PowerShell as your user and run:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Then try the activation command again:

.\venv\Scripts\Activate.ps1
macOS or Linux
Create the virtual environment:

python3 -m venv venv
Activate it:

source venv/bin/activate
Installing Dependencies
Make sure the virtual environment is activated.

Install Flask using
requirements.txt
:

pip install -r requirements.txt
If your system uses
pip3
, run:

pip3 install -r requirements.txt
You can verify that Flask was installed with:

pip show Flask
Running the Flask Application
Make sure you are inside the project folder and that the virtual environment is active.

Run:

python app.py
The application should start at:

http://localhost:5000
You should see output similar to:

* Running on http://localhost:5000
Keep this terminal window open while using the API.

To stop the application, press:

CTRL+C
Server URL
The CodeCraftHub API runs at:

http://localhost:5000
The API endpoint prefix is:

http://localhost:5000/api
API Documentation
Course Fields
Each course contains the following fields:

Field	Description	Example
id
Automatically generated positive integer	
1
name
Course name	
"Learn Flask"
description
Course description	
"Build REST APIs with Flask."
target_date
Target completion date using
YYYY-MM-DD
"2026-12-31"
status
Current course status	
"Not Started"
created_at
Automatically generated timestamp	
"2026-10-08T14:30:00+00:00"
Allowed status values are exactly:

Not Started
In Progress
Completed
Endpoint Summary
HTTP method	Endpoint	Purpose
POST
/api/courses
Create a new course
GET
/api/courses
Get all courses
GET
/api/courses/<id>
Get one course
PUT
/api/courses/<id>
Update one course
DELETE
/api/courses/<id>
Delete one course
The
<id>
value must be a positive integer, such as:

1
1. Create a Course
Request
POST /api/courses
The request must use the following header:

Content-Type: application/json
JSON request body
{
  "name": "Learn Flask",
  "description": "Build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
The client should not provide:

id
created_at
These fields are generated automatically by the server.

Windows PowerShell command
curl.exe -X POST http://localhost:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{"name":"Learn Flask","description":"Build REST APIs with Flask.","target_date":"2026-12-31","status":"Not Started"}'
Windows Command Prompt command
curl.exe -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Learn Flask\",\"description\":\"Build REST APIs with Flask.\",\"target_date\":\"2026-12-31\",\"status\":\"Not Started\"}"
Successful response
Status:

201 Created
Example:

{
  "id": 1,
  "name": "Learn Flask",
  "description": "Build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-10-08T14:30:00+00:00"
}
The exact
created_at
value will be different.

2. Get All Courses
Request
GET /api/courses
Windows PowerShell command
curl.exe -X GET http://localhost:5000/api/courses
Windows Command Prompt command
curl.exe -X GET http://localhost:5000/api/courses
Successful response
Status:

200 OK
Example:

[
  {
    "id": 1,
    "name": "Learn Flask",
    "description": "Build REST APIs with Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-10-08T14:30:00+00:00"
  }
]
If no courses exist, the response is:

[]
3. Get One Course
Request
GET /api/courses/1
Windows PowerShell command
curl.exe -X GET http://localhost:5000/api/courses/1
Windows Command Prompt command
curl.exe -X GET http://localhost:5000/api/courses/1
Successful response
Status:

200 OK
Example:

{
  "id": 1,
  "name": "Learn Flask",
  "description": "Build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-10-08T14:30:00+00:00"
}
4. Update a Course
The
PUT
endpoint replaces the editable details of a course.

All editable fields are required:

name
description
target_date
status
The following fields must not be changed by the client:

id
created_at
Request
PUT /api/courses/1
JSON request body
{
  "name": "Advanced Flask",
  "description": "Build complete Flask REST APIs.",
  "target_date": "2027-01-31",
  "status": "In Progress"
}
Windows PowerShell command
curl.exe -X PUT http://localhost:5000/api/courses/1 `
  -H "Content-Type: application/json" `
  -d '{"name":"Advanced Flask","description":"Build complete Flask REST APIs.","target_date":"2027-01-31","status":"In Progress"}'
Windows Command Prompt command
curl.exe -X PUT http://localhost:5000/api/courses/1 -H "Content-Type: application/json" -d "{\"name\":\"Advanced Flask\",\"description\":\"Build complete Flask REST APIs.\",\"target_date\":\"2027-01-31\",\"status\":\"In Progress\"}"
Successful response
Status:

200 OK
Example:

{
  "id": 1,
  "name": "Advanced Flask",
  "description": "Build complete Flask REST APIs.",
  "target_date": "2027-01-31",
  "status": "In Progress",
  "created_at": "2026-10-08T14:30:00+00:00"
}
The
id
and
created_at
values remain unchanged.

5. Delete a Course
Request
DELETE /api/courses/1
Windows PowerShell command
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
Windows Command Prompt command
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
The
-i
option displays the HTTP response headers, including the status code.

Successful response
Status:

204 No Content
There is no response body when deletion succeeds.

Validation and Error Handling
The API validates all incoming course data.

Required fields
The following fields are required when creating or updating a course:

name
description
target_date
status
If a required field is missing, the API returns:

400 Bad Request
Example response:

{
  "error": "Missing required field(s): description, status, target_date"
}
Empty fields
The following values are rejected:

{
  "name": "",
  "description": "   ",
  "target_date": "",
  "status": ""
}
Example response:

{
  "error": "name cannot be empty"
}
Target date validation
The
target_date
must use this format:

YYYY-MM-DD
Valid example:

2026-12-31
Invalid examples:

12/31/2026
31-12-2026
2026-2-1
2026-02-30
Example error:

{
  "error": "target_date must use YYYY-MM-DD format"
}
Status validation
The status must exactly match one of these values:

Not Started
In Progress
Completed
These examples are invalid:

started
finished
Done
complete
Example error:

{
  "error": "status must be exactly \"Not Started\", \"In Progress\", or \"Completed\""
}
Invalid course IDs
Course IDs must be positive integers.

Valid IDs:

1
2
25
Invalid IDs:

0
-1
abc
1.5
Example response:

{
  "error": "Course ID must be a positive integer"
}
Status:

400 Bad Request
Course not found
If the ID is valid but no course exists with that ID, the API returns:

404 Not Found
Example response:

{
  "error": "Course not found"
}
Invalid JSON
Requests must contain valid JSON.

Invalid example:

{
  "name": "Broken JSON"
The closing brace is missing.

Example response:

{
  "error": "Request body contains invalid JSON"
}
Status:

400 Bad Request
Missing Content-Type Header
JSON requests must include:

Content-Type: application/json
If this header is missing, the API returns:

{
  "error": "Request Content-Type must be application/json"
}
HTTP Status Code Summary
Situation	Status code
Course created successfully	
201 Created
Data retrieved successfully	
200 OK
Course updated successfully	
200 OK
Course deleted successfully	
204 No Content
Invalid input	
400 Bad Request
Invalid JSON	
400 Bad Request
Invalid course ID	
400 Bad Request
Course not found	
404 Not Found
JSON file read or write error	
500 Internal Server Error
How
courses.json
Provides Persistence
CodeCraftHub uses
courses.json
to store course data.

The file is located in the same folder as
app.py
.

Example:

[
  {
    "id": 1,
    "name": "Learn Flask",
    "description": "Build REST APIs with Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-10-08T14:30:00+00:00"
  }
]
Reading data
When the API receives a
GET
request, it reads the courses from
courses.json
.

Creating data
When a course is created, the API:

Reads the current courses.
Generates a new ID.
Adds the new course.
Writes the updated list back to
courses.json
.
Updating data
When a course is updated, the API:

Reads the current courses.
Finds the course by ID.
Changes its editable fields.
Saves the updated list.
Deleting data
When a course is deleted, the API:

Reads the current courses.
Finds the course by ID.
Removes it from the list.
Saves the updated list.
The file is created automatically if it does not already exist.

Because the data is saved to a file, courses remain available after the Flask application is stopped and started again.

Testing the API
Start the application
Run:

python app.py
Keep the application running.

Open another terminal
Use a second terminal window to run the API requests.

Recommended test order
Create a course with
POST
.
Get all courses with
GET
.
Get the created course by ID.
Update the course with
PUT
.
Get the course again to verify the update.
Delete the course.
Get the course again to verify it was deleted.
Test creating a course
PowerShell
curl.exe -X POST http://localhost:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{"name":"Python Basics","description":"Learn the fundamentals of Python.","target_date":"2026-12-15","status":"Not Started"}'
Command Prompt
curl.exe -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Python Basics\",\"description\":\"Learn the fundamentals of Python.\",\"target_date\":\"2026-12-15\",\"status\":\"Not Started\"}"
Expected status:

201 Created
Record the returned
id
.

Test retrieving all courses
PowerShell
curl.exe -X GET http://localhost:5000/api/courses
Command Prompt
curl.exe -X GET http://localhost:5000/api/courses
Expected status:

200 OK
Test updating a course
Replace
1
with the ID returned when the course was created.

PowerShell
curl.exe -X PUT http://localhost:5000/api/courses/1 `
  -H "Content-Type: application/json" `
  -d '{"name":"Advanced Python","description":"Learn more advanced Python topics.","target_date":"2027-01-15","status":"In Progress"}'
Command Prompt
curl.exe -X PUT http://localhost:5000/api/courses/1 -H "Content-Type: application/json" -d "{\"name\":\"Advanced Python\",\"description\":\"Learn more advanced Python topics.\",\"target_date\":\"2027-01-15\",\"status\":\"In Progress\"}"
Expected status:

200 OK
Test deleting a course
PowerShell
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
Command Prompt
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
Expected status:

204 No Content
Test persistence
Create a course.

Check that it appears in
courses.json
.

Stop the application using
CTRL+C
.

Start the application again:

python app.py
Request all courses again:

PowerShell
curl.exe -X GET http://localhost:5000/api/courses
Command Prompt
curl.exe -X GET http://localhost:5000/api/courses
The course should still be present.

View
courses.json
Windows PowerShell
Get-Content .\courses.json
Windows Command Prompt
type courses.json
macOS or Linux
cat courses.json
Troubleshooting
Problem:
python
is not recognized
Try:

python3 --version
If that works, use
python3
instead of
python
.

For example:

python3 app.py
On Windows, make sure Python was added to the system PATH during installation.

Problem: Flask is not installed
Activate the virtual environment and run:

pip install -r requirements.txt
You can check whether Flask is installed with:

pip show Flask
Problem: The virtual environment is not active
After activation, the terminal should show
(venv)
.

Windows Command Prompt:

venv\Scripts\activate
Windows PowerShell:

.\venv\Scripts\Activate.ps1
macOS or Linux:

source venv/bin/activate
Problem: Port 5000 is already in use
Another program may already be using port
5000
.

Stop the other application, then try running CodeCraftHub again.

You can also check whether another CodeCraftHub process is already running.

Problem:
Connection refused
Make sure the Flask application is running:

python app.py
Also verify that the URL is correct:

http://localhost:5000
Problem:
courses.json
does not exist
The application should create it automatically when started.

Make sure:

You are running
app.py
.
The application has permission to create files in the project folder.
You are checking the same folder that contains
app.py
.
Problem:
courses.json
contains invalid JSON
Do not manually add comments to a JSON file.

For example, this is invalid JSON:

[
  {
    "id": 1,
    "name": "Learn Flask"
  }
  // This is not allowed in JSON
]
JSON does not support comments.

If the file is damaged and you do not need the existing course data, stop the application, replace the contents with:

[]
Then start the application again.

Problem: A request returns
400 Bad Request
Check that:

The request body is valid JSON.
The
Content-Type
header is included.
All required fields are present.
No required field is empty.
target_date
uses
YYYY-MM-DD
.
status
exactly matches an allowed status.
Problem: A request returns
404 Not Found
Check that:

The URL is correct.
The course ID exists.
The course ID is a positive integer.
The route includes
/api/courses
.
Example:

http://localhost:5000/api/courses/1
Uploading CodeCraftHub to GitHub
GitHub can be used to store and share the project source code.

Step 1: Create a GitHub repository
Sign in to GitHub.

Select New repository.

Enter a repository name, such as:

codecrafthub
Add a short description.

Choose whether the repository should be public or private.

Create the repository.

Do not add extra files if the project already contains a
README.md
.

Step 2: Initialize Git locally
Open a terminal inside the CodeCraftHub project folder.

Run:

git init
Step 3: Add project files
git add app.py requirements.txt README.md courses.json
If
courses.json
does not exist yet, add only the files that are present:

git add app.py requirements.txt README.md
Step 4: Create the first commit
git commit -m "Initial CodeCraftHub project"
Step 5: Connect the local project to GitHub
Copy the repository URL from GitHub.

It will look similar to:

https://github.com/your-username/codecrafthub.git
Run:

git remote add origin https://github.com/your-username/codecrafthub.git
Replace
your-username
with your GitHub username.

Step 6: Rename the main branch
git branch -M main
Step 7: Upload the project
git push -u origin main
Refresh the GitHub repository page to see the uploaded files.

Future Updates
After making changes, use:

git add .
git commit -m "Describe your changes"
git push
For example:

git add .
git commit -m "Improve course validation"
git push
Important File Note
The project stores data in
courses.json
.

If you do not want to upload your local course data, you can create a
.gitignore
file containing:

venv/
__pycache__/
The
courses.json
file may be included if you want the repository to contain sample course data. Alternatively, you can create an empty
courses.json
file containing:

[]
This keeps the project simple and allows the application to start with no courses.

undefined