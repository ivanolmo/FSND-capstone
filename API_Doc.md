# API Usage
The API can be accessed at **https://baseball-agency-api.herokuapp.com**.

### Testing and mock data  
Mock data has been loaded into the database so that `DELETE` endpoints function correctly during testing. Running 
curl or Postman tests will alter database data (unittests do not), so it's recommended to run any tests on a secondary 
_test_ database so that the live database won't be affected. The test database can be dropped and recreated for the 
next round of testing, if necessary. The mock data were given an `id` of 500 to distinguish them from the rest of the data.

Mock data:

    /players/500
    {
        "id": 500,
        "name": "Alex Verdugo",
        "number": "99",
        "position": "Right Field",
        "salary": "583,000 USD",
        "team_id": 1,
        "agent_id": 1
    }
    
    /teams/500
    {
        "id": 500,
        "name": "Boston Red Sox",
        "abbr": "BOS",
        "city": "Boston",
        "state": "MA",
        "total_payroll": "180.4 million USD"
    }
    
    /agents/500
    {
        "id": 500,
        "name": "Dan Lozano",
        "salary": "250,000 USD"
    }

### Error handling
Errors are returned as a JSON object, and are formatted as follows:

    {
        "success": False,
        "error": 400,
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }

The API will return one of the following errors when a request fails:

    - 400 -- Bad Request - The request could not be understood by the server
    - 404 -- Not Found - The requested resource could not be found
    - 405 -- Method Not Allowed - The specified method is not allowed for the endpoint
    - 500 -- Internal Server Error - The server encountered an unexpected condition

Additionally, any errors related to authentication will return one of the
 following:

    - 401 -- Unauthorized - The server could not verify your authorization.
    - 403 -- Forbidden - Authorized, but you don't have permission to access the requested resource.


### Database Schema

Here is a representation of the db schema ([`models.py`](./models.py)):

    players
    - id (primary key)
    - name
    - number
    - position
    - salary
    - team_id (foreign key to teams.id)
    - agent_id (foreign key to agents.id)
    ```
    ```
    teams
    - id (primary key, links to players table through players.team_id)
    - name
    - abbreviation
    - city
    - state
    - total_payroll
    ```
    ```
    agents
    - id (primary key, links to players table through players.agent_id)
    - name
    - salary

Every field must be populated. Constraints are enforced in the backend so that no fields are null. A `player`
cannot be inserted if the `team_id` or `agent_id` do not already exist in the database. Additionally,
no `team` or `agent` can be deleted if either has a `player` assigned to it.  

### Role Based Access Control
There are 3 roles utilized in this project. They are `agent_assistant`, `agent`, and `executive_agent`. 
All endpoints except one will require the user to be authenticated with one of the roles listed above.  
#### Permission Overview
##### agent_assistant  
The agent assistant assists an agent in day to day operations, and thus needs access to player lists 
and player details, team rosters, and a list of agents.

    - get:player-details
    - get:teams
    - get:team-roster
    - get:agents

##### agent  
An agent is what makes the business run. They sign new players, so in addition to an assistants 
permissions, an agent can also post, patch, or delete players and teams.

    - *all permissions above, plus:*
    - get:team-details
    - post:players
    - post:teams
    - patch:players
    - patch:teams
    - delete:players
    - delete:teams

##### executive_agent  
An executive agent is in charge of the big picture. They're not overly concerned with adding new 
players or teams, so they don't possess those permissions. Instead, they can post, patch, or delete
an agent, as well as get agent specific details and their client list.

    - *all GET permissions above, plus:*
    - get:agent-details
    - get:agent-clients
    - post:agents
    - patch:agents
    - delete:agents

With the exception of `GET /players`, all endpoints will require authentication using a JWT Bearer token. 
Credentials and a JWT bearer token can be obtained by visiting:

    https://baseball-agency.auth0.com/authorize?audience=baseball-agency-api&response_type=token&client_id=pMeaPUNuDQgXjKVckrdVLkYZYVw3cZpx&redirect_uri=https://baseball-agency-api.herokuapp.com

Users have already been set up with each of the 3 available roles (credentials will be provided 
in the project submission details). Once logged in, the JWT Bearer token can be extracted from the URL 
bar in your browser. Use that bearer token to access the API endpoints.

## Requests
The Baseball Agency API endpoints are accessed using HTTP requests and JSON request bodies. Each endpoint uses the 
appropriate HTTP verb for the action it performs. This API utilizes the `GET`, `POST`, `PATCH`, and `DELETE` methods. 
The most convenient method of accessing this API is using the Postman tool, however, the `curl` tool is also an option.

**Method/Action**  

    - GET - retrieve players, player details, teams, team details, team roster, agents, agent details, and agent clients
    - POST - create a new player, team, or agent
    - PATCH - patch an existing player, team, or agent
    - DELETE - delete an existing player, team, or agent

**Responses**  
The API will return one of the following status codes when a request succeeds:

    - 200 -- OK - request successful
    - 201 -- Created - a new resource was created successfully

# Endpoint Overview
## GET
#### GET /players  
- Only endpoint that doesn't require authentication.
- Returns a paginated list of all players in the database, with 10 players per page.
- An optional argument can be appended to the end of the query to get a specific page of players.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/players`
    - With optional argument: `curl https://baseball-agency-api.herokuapp.com/players?page=7`
    - Sample response:
    ```
    {
        "players": [
            {
                "id": "1",
                "name": "Baseball Player",
                "number": "10",
                "position": "Pitcher",
                "team_id": 1
            },
            {
                next 9 players...
            }
        ],
        "success": true,
        "total_players": 100
    }
    ```

#### GET /player/<int:id>/details
- Requires authentication (`agent_assistant` user or above).
- Returns specific details for the player, which includes the additional `salary` field.
- The endpoint will return a status code of 200 if successful, or 404 if no player is found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/players/1/details -H "Authorization-Type: Bearer (insert bearer token here)"`
    - Sample response:
    ```
    {
        "player_details": {
                "agent_id": 1,
                "id": "1",
                "name": "Baseball Player",
                "number": "10",
                "position": "Pitcher",
                "salary": "1 million USD",
                "team_id": 1
        },
        "success": true
    }
    ```

#### GET /teams
- Requires authentication (`agent_assistant` user or above).
- Returns a list of all teams in the database.
- The endpoint will return a status code of 200 if successful, or 404 if no teams are found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/teams -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "success": true,
        "teams": [
            {
                "abbr": "ABC",
                "city": "Some Town",
                "id": 1,
                "name": "Some Town Ballers",
                "state": "Some State"
            },
            {
                next team...
            }
        ],
        "total_teams": 5
    }
    ```

#### GET /teams/<int:id>/details
- Requires authentication (`agent` user or above).
- Returns specific details for the team, which includes the additional `total_payroll` field.
- The endpoint will return a status code of 200 if successful, or 404 if no team is found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/teams -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "success": true,
        "team_details": {
            "abbr": "ABC",
            "city": "Some Town",
            "id": 1,
            "name": "Some Town Ballers",
            "state": "Some State",
            "total_payroll": "SO. MUCH. MONEY"
        }
    }
    ```

#### GET /teams/<int:id>/roster
- Requires authentication (`agent_assistant` user or above).
- Returns a team's complete player roster, including the id, name, number, and position of each player.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/teams/1/roster -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "roster": [
            {
                "id": 1,
                "name": "Baseball Player",
                "number": "1",
                "position": "Pitcher",
                "team_id": 1
            },
            {
                next player...
            },
            {
                last player...
            }
        ],
        "success": true,
        "team": "Some Town Ballers",
        "total_team_players": 27
    }
    ```

#### GET /agents
- Requires authentication (`agent` user or above).
- Returns a list of all agents in the database. This endpoint only shows name and id.
- The endpoint will return a status code of 200 if successful, or 404 if no agents are found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/agents -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "agents": [
            {
                "id": 1,
                "name": "Superstar Agent"
            },
            {
                "id": 2,
                "name": "Rockstar Agent"
            },
            {
                next agent...
            }
        ],
        "success": true,
        "total_agents": 10
    }
    ```

#### GET /agents/<int:id>/details
- Requires authentication (`executive_agent` user only).
- Returns specific details for the agent, which includes the additional `salary` field.
- The endpoint will return a status code of 200 if successful, or 404 if no agent is found.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/agents/1/details -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "agent": {
            "id": 1,
            "name": "Superstar Agent",
            "salary": "10 million USD"
        },
        "success": true
    }
    ```

#### GET /agents/<int:id>/clients
- Requires authentication (`executive_agent` user only).
- Returns the player/client list for one agent, including the id, name, number, and position of each player.
- The endpoint will return a status code of 200 if successful, or 404 if no player/clients are assigned to the agent.

    - Sample usage: `curl https://baseball-agency-api.herokuapp.com/agents/1/clients -H 'Authorization: Bearer (insert bearer token here)'`
    - Sample response:
    ```
    {
        "agent": "Superstar Agent",
        "clients": [
            {
                "id": 1,
                "name": "Baseball Player",
                "number": "1",
                "position": "Pitcher",
                "team_id": 1
            },
            {
                "id": 5,
                "name": "Baseball Slugger",
                "number": "99",
                "position": "First Base",
                "team_id": 4
            },
            {
                next player/client...
            }
        ],
        "success": true,
        "total_agent_clients": 19
    }
    ```

## POST
#### POST /players
- Requires authentication (`agent` user only).
- Will insert a new player into the database if the json body is valid.
- The endpoint will return a status code of 201 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- All fields in the request body are required and cannot be empty.
- `team_id` and `agent_id` are integers and must already exist in the database.
- `name`, `number`, `position`, and `salary` are string fields.
  
    - Sample request body format:
    ```
    {
        "name": "Baseball Player",
        "number": "10",
        "position": "Pitcher",
        "salary": "1 million USD",
        "team_id": 1,
        "agent_id": 1
    }
    ```
    - Sample usage: `curl -X POST https://baseball-agency-api.herokuapp.com/players -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "Baseball Player", "number": "10", "position": "Pitcher",
      "salary": "1 million USD", "team_id": 1, "agent_id": 1}'`
    - Sample response:
    ```
    {
        "new_player": {
            "agent_id": 1,
            "id": "1",
            "name": "Baseball Player",
            "number": "10",
            "position": "Pitcher",
            "salary": "1 million USD",
            "team_id": 1
        },
        "new_player_id": 1,
        "success": true,
        "total_players": 101
    }
    ```
  
#### POST /teams
- Requires authentication (`agent` user only).
- Will insert a new team into the database if the json body is valid.
- The endpoint will return a status code of 201 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- All fields in the request body are required and cannot be empty.
- All fields are string fields.
  
    - Sample request body format:
    ```
    {
        "name": "Some Town Ballers",
        "abbr": "ABC",
        "city": "Some Town",
        "state": "Some State",
        "total_payroll": "100 million USD"
    }
    ```
    - Sample usage: `curl -X POST https://baseball-agency-api.herokuapp.com/teams -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "Some Town Ballers", "abbr": "ABC", "city": "Some Town", "state": 
      "Some State", "total_payroll": "100 million USD"}'`
    - Sample response:
    ```
    {
        "new_team": {
            "abbr": "ABC",
            "city": "Some Town",
            "id": "1",
            "name": "Some Town Ballers",
            "state": "Some State",
            "total_payroll": "100 million USD"
        },
        "new_team_id": 1,
        "success": true,
        "total_teams": 5
    }
    ```

#### POST /agents
- Requires authentication (`executive_agent` user only).
- Will insert a new agent into the database if the json body is valid.
- The endpoint will return a status code of 201 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- All fields in the request body are required and cannot be empty.
- All fields are string fields.
  
    - Sample request body format:
    ```
    {
        "name": "Superstar Agent",
        "salary": "1 million USD"
    }
    ```
    - Sample usage: `curl -X POST https://baseball-agency-api.herokuapp.com/agents -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "Superstar Agent", "salary": "1 million USD"}'`
    - Sample response:
    ```
    {
        "new_agent": {
            "id": 1,
            "name": "Superstar Agent",
            "salary": "1 million USD"
        },
        "new_agent_id": 1,
        "success": true,
        "total_agents": 11
    }
    ```

## PATCH
#### PATCH /players/<int:id>
- Requires authentication (`agent` user only).
- Will patch an existing player ID in the database if the json body is valid.
- The endpoint will return a status code of 200 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- You can pick and choose which field(s) to edit, i.e. one, some, or all fields can be edited simultaneously.
- `team_id` and `agent_id` are integers and must already exist in the database (if included in the request body).
- `name`, `number`, `position`, and `salary` are string fields and cannot be empty (if included in the request body).
  
    - Sample request body format:
    ```
    {
        "name": "Baseball Guy",
        "number": "99",
        "position": "Catcher",
        "salary": "5 million USD",
        "team_id": 5,
        "agent_id": 9
    }
    ```
    - Sample usage: `curl -X PATCH https://baseball-agency-api.herokuapp.com/players/1 -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "Baseball Guy", "number": "99", "position": "Catcher",
      "salary": "5 million USD", "team_id": 5, "agent_id": 9}'`
    - Sample response:
    ```
    {
        "success": true,
        "updated_player": {
            "agent_id": 9,
            "id": "1",
            "name": "Baseball Guy",
            "number": "99",
            "position": "Catcher",
            "salary": "5 million USD",
            "team_id": 5
        },
    }
    ```
  
#### PATCH /teams/<int:id>
- Requires authentication (`agent` user only).
- Will patch an existing team ID in the database if the json body is valid.
- The endpoint will return a status code of 200 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- You can pick and choose which field(s) to edit, i.e. one, some, or all fields can be edited simultaneously.
- All fields are string fields and cannot be empty (if included in the request body).
  
    - Sample request body format:
    ```
    {
        "name": "That Town Aces",
        "abbr": "XYZ",
        "city": "That Town",
        "state": "Whatever State",
        "total_payroll": "250 million USD"
    }
    ```
    - Sample usage: `curl -X PATCH https://baseball-agency-api.herokuapp.com/teams/1 -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "That Town Aces", "abbr": "XYZ", "city": "That Town", "state": 
      "Whatever State", "total_payroll": "250 million USD"}'`
    - Sample response:
    ```
    {
        "success": true,
        "updated_team": {
            "abbr": "XYZ",
            "city": "That Town",
            "id": "1",
            "name": "That Town Aces",
            "state": "Whatever State",
            "total_payroll": "250 million USD"
        },
    }
    ```

#### PATCH /agents/<int:id>
- Requires authentication (`executive_agent` user only).
- Will patch an existing agent in the database if the json body is valid.
- The endpoint will return a status code of 200 if successful, 400 if the request is malformed, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- You can pick and choose which field(s) to edit, i.e. one or both fields can be edited simultaneously.
- Both fields are string fields and cannot be empty (if included in the request body).
  
    - Sample request body format:
    ```
    {
        "name": "Flashiest Agent",
        "salary": "5 million USD"
    }
    ```
    - Sample usage: `curl -X PATCH https://baseball-agency-api.herokuapp.com/agents/1 -H 'Authorization: Bearer (insert bearer token here)'
      -H 'content-type: application/json' -d '{"name": "Flashiest Agent", "salary": "5 million USD"}'`
    - Sample response:
    ```
    {
        "success": true,
        "updated_agent": {
            "id": 1,
            "name": "Flashiest Agent",
            "salary": "5 million USD"
        },
    }
    ```

## DELETE
#### DELETE /players/<int:id>
- Requires authentication (`agent` user only).
- Will delete an existing player id from the database.
- The endpoint will return a status code of 200 if successful, 404 if the player id isn't found, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.

    - Sample usage: `curl -X DELETE https://baseball-agency-api.herokuapp.com/players/1`
    - Sample response:
    ```
    {
        "deleted_id": 1,
        "success": true,
        "total_players": 100
    }
    ```
  
#### DELETE /teams/<int:id>
- Requires authentication (`agent` user only).
- Will delete an existing team from the database.
- The endpoint will return a status code of 200 if successful, 404 if the team id isn't found, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- **IMPORTANT** A team _cannot_ be removed if any player has a team_id equal to the team id you're trying to delete.
- In the above case, a response will be returned informing the user the team has one (or more) player(s) assigned, and will also
  return a list of any assigned player(s).

    - Sample response when trying to delete a team with one (or more) player(s) assigned to it:
    ```
    {
        "message": "This team currently has one or more players. Please reassign those players before deleting this team!",
        "players": [
            list of players...
        ],
        "success": false,
        "total_players": 30
    }
    ```
    - Sample usage: `curl -X DELETE https://baseball-agency-api.herokuapp.com/teams/1`
    - Sample response:
    ```
    {
        "deleted_id": 1,
        "success": true,
        "total_teams": 4
    }
    ```

#### DELETE /agents/<int:id>
- Requires authentication (`executive_agent` user only).
- Will delete an existing agent from the database.
- The endpoint will return a status code of 200 if successful, 404 if the agent id isn't found, 401 if no authorization 
  header is present, or 403 if authorization is present but permission is not found.
- **IMPORTANT** An agent _cannot_ be removed if any player has an agent_id equal to the agent id you're trying to delete.
- In the above case, a response will be returned informing the user the agent has one (or more) player(s) assigned, and will also
  return a list of any assigned player(s).

    - Sample response when trying to delete an agent with one (or more) player(s) assigned to it:
    ```
    {
        "clients": [
            list of player/clients...
        ],
        "message": "This agent currently represents one or more players. Please reassign those players before deleting this agent!",
        "success": false,
        "total_clients": 21
    }
    ```
    - Sample usage: `curl -X DELETE https://baseball-agency-api.herokuapp.com/agents/1`
    - Sample response:
    ```
    {
        "deleted_id": 1,
        "success": true,
        "total_agents": 10
    }
    ```