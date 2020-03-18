# Full Stack Nanodegree Capstone Project

## Baseball Player Agency

### Intro
This is the final project for the Udacity Full Stack Nanodegree. This project
consists of an API with a Python backend, and stores data in a Postgresql
database. This project will also incorporate third-party authentication with
Role Based Access Control using Auth0. The project doesn't utilize a frontend at
this time.

The premise of the baseball_agency API is a system that holds `player`, `team`, 
and `agent` information. Various data are stored about each entity, and are
linked using db relationships. The db included in this project has full
rosters for 5 major league teams, information on those teams, as well as 10
agents.

Players are assigned to their real life teams, but randomly assigned to
agents. When a player is added to the database, a `team_id` and `agent_id` 
are **required**. Additionally, an agent or team can't be deleted from the
database if players are assigned to either. A player can only be assigned to
one team or agent, but a team or agent can have many players assigned
to them.

Each player has the following attributes:
```
name
number
position
salary
team_id
agent_id
```
Each team has the following attributes:
```
name
abbreviation
city
state
total_payroll
```
Each agent has the following attributes:
```
name
salary
```  
A player, team, or agent can be queried on an individual basis to
retrieve more information on them. A team can be queried for it's roster, and 
an agent can be queried to find their client list. All endpoints except `GET /players`
require authorization using a standard JWT Bearer token. Information on authorization
and obtaining a token are found in the.

#### RBAC
Each endpoint is access controlled using Auth0's Role Based Access Control
(RBAC), with the exception of one publicly accessible endpoint. Specifics on
each role and the permissions granted to each are in the API documentation at
[API_Doc](./API_Doc.md).

### Installing Dependencies
#### Python 3.7
Follow instructions to install the correct version of Python for your platform
in the [python docs](https://docs.python.org/3/using/index.html).

#### Virtual Environment (venv)
We recommend working within a virtual environment whenever using Python for 
projects. This keeps your dependencies for each project separate and organaized.
Instructions for setting up a virual enviornment for your platform can be found 
in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependecies
Once you have your venv setup and running, install dependencies by navigating
 to the root directory and running:
 ```
 pip install -r requirements.txt
```
This will install all of the required packages included in the `requirements.txt`
file.

#### Local Database Setup
With the Postgres server running locally, you can populate a new database using 
the `baseball.psql` file included in the root directory. Use your terminal to
restore the included file. **_The new database must first be created_**. Once 
you create the database, open your terminal, navigate to the root folder, and run:

`psql -U postgres -d YourDatabaseName -f baseball.psql`

or

`psql baseball < baseball.psql`

The new database will now be populated with 5 teams, their full rosters, and
10 agents. Further information on Postgresql usage can be found [in the docs
](https://www.postgresql.org/docs/12/index.html).

#### Environment Variables
All variables are stored locally in the `.env` file. Take a look at the 
`.env.example` file for a representation of what your `.env` file should look 
like. Please ensure the `DATABASE_URL` is accurate for your system if running
this project locally.

#### Local Testing
To test your local installation, run the following command from the root folder:  
    
    pytest

If all tests pass, your local installation is set up correctly.

#### Running the server
From within the root directory, first ensure you're working with your created
venv. To run the server, execute the following:
```
export FLASK_APP=baseball_agency
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and
restart the server automatically.   
Setting the `FLASK_APP` variable to `baseball_agency` directs Flask to use
the `baseball_agency` directory and the `__init__.py` file to find and load the
application.

### Please see the documentation on API usage at [`API_Doc.md`](./API_Doc.md).
