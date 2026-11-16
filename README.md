# COMP3005 Assignment 3 Question 1

Name: Chizurum Oluigbo\
Student #: 101361390\
SECTION: COMP3005A

**Link to video description:**  

## Setting up Postgres connection
- In pgAdmin, right-click **Databases** -> **Create** -> **Database...** and create an empty database named `assignment3`.
- Right click `assignment3`, click **Query Tool**
- Click the folder icon, open `students.sql`, and run it to create the `students` table and insert the sample rows

## Running the application
- Open a terminal in the `COMP3005A-Assignment3` folder
- In terminal, create and activate a virtual environment:
 ```bash
 python -m venv .venv
 ```
- In terminal, activate .venv using 
    - Windows Powershell: `.venv\Scripts\Activate.ps1`
    - Windows cmd: `.venv\Scripts\activate.bat`
    - macOS/Linus: `source .venv/bin/activate`
- Install dependencies:
 ```bash
 pip install -r requirements.txt
 ```
- Copy the example environment file:
 ```bash
 copy .env.example .env
 ```

 (Use `cp` on macOS/Linux. Fill in placeholders DB_USER and DB_PASSWORD in .env with your user and password. You may alter the default values of the others if yours differ.)
- Run the app:
 ```bash
 python app\app.py
 ```