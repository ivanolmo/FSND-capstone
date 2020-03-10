# API Usage
### Error handling
Errors are returned as a JSON object, and are formatted as follows:
```
{
    "success": False,
    "error": 400,
    "message": "The browser (or proxy) sent a request that this server could not understand."
}
```

The API will return one of the following errors when a request fails:
```
- 400 -- Bad Request - The request could not be understood by the server
- 404 -- Not Found - The requested resource could not be found
- 405 -- Method Not Allowed - The specified method is not allowed for the endpoint
- 500 -- Internal Server Error - The server encountered an unexpected condition
```
Additionally, any errors related to authentication will return one of the
 following:
```
- 401 -- Unauthorized - The server could not verify your authorization.
- 403 -- Forbidden - Authorized, but you don't have permission to access the requested resource.
```

### Database Schema

Here is a representation of the db schema (`models.py`):
```
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
```
Every field must be populated, so `NOT NULL` constraints are enforced in the backend. A `player`
cannot be inserted if the `team_id` or `agent_id` do not already exist in the database. Additionally,
no `team` or `agent` can be deleted if either has a `player` assigned to it.


### Role Based Access Control
There are 3 roles utilized in this project. They are `agent_assistant
`, `agent`, and `executive_agent`. All endpoints except one will require the
 user to be authenticated with one of the roles listed above.  
##### Permission Overview
#### agent_assistant  
The agent assistant assists an agent in day to day operations, and thus
needs access to player lists and player details, team rosters, and a list of
agents.
- `get:player-details`
- `get:teams`
- `get:team-roster`
- `get:agents`

#### agent  
An agent is what makes the business run. They sign new players, so in
addition to an assistants permissions, an agent can also post, patch, or
delete players and teams.
- *all permissions above, plus:*
- `get:team-details`
- `get:agent-clients`
- `post:players`
- `post:teams`
- `patch:players`
- `patch:teams`
- `delete:players`
- `delete:teams`

#### executive_agent  
An executive agent is in charge of the big picture. They're not overly
concerned with specific players or teams, so they don't require those
permissions. Instead, they can post, patch, or delete agents, as well as
get an agents specific details.
- *all `GET` operations above, plus:*
- `get:agent-details`
- `post:agents`
- `patch:agents`
- `delete:agents`

With the exception of `GET /players`, all endpoints will require authentication using a JWT Bearer token. 
Credentials and a JWT bearer token can be obtained by visiting:

    https://baseball-agency.auth0.com/authorize?audience=baseball-agency-api&response_type=token&client_id=pMeaPUNuDQgXjKVckrdVLkYZYVw3cZpx&redirect_uri=http://localhost:5000

Users have already been set up with each of the 3 available roles (credentials will be provided 
in the submission details). Once logged in, the JWT Bearer token can be extracted from the URL 
bar in your browser. Use that bearer token to access the API endpoints.

## Requests
The Baseball Agency API endpoints are accessed using HTTP requests. Each endpoint uses the 
appropriate HTTP verb for the action it performs. This API utilizes the `GET`, `POST`, `PATCH`, 
and `DELETE` methods. The most convenient method of accessing this API is using the Postman tool,
however, the `curl` tool is also an option.

**Method/Action**
```
- GET - retrieves players, player details, teams, team details, team roster, agents, agent details, and agent clients
- POST - creates new players, teams, or agents
- PATCH - patches existing players, teams, or agents
- DELETE - deletes existing players, teams, or agents
```

**Responses**\
The API will return one of the following status codes when a request succeeds:
```
- 200 - OK - request successful
- 201 - Created - a new resource was created successfully
```
## Endpoint Overview
#### GET /players  
- Only endpoint that doesn't require authentication
- Returns a paginated list of all players in the database, with 10 players per page
- An optional argument can be appended to the end of the query to get a specific page of players
- The endpoint will return a status code of 200 if successful, or 404 if no players are found

    - Sample usage: `curl http://localhost:5000/players`
    - With optional argument: `curl http://localhost:5000/players?page=7`
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
            next player...
        }
    ],
    "success": true,
    "total_players": 100
}
```

#### GET /player/<int:player_id>/details
- Requires authentication.
- Returns one players specific details, which includes player salary.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.
    - Sample usage: `curl http://localhost:5000/players/1/details -H "Authorization-Type: Bearer (insert bearer token here)"`
    - Sample response:
```
{
    "player_details": {
            "agent_id": 1,
            "id": "1",
            "name": "Baseball Player",
            "number": "10",
            "position": "Pitcher",
            "salary": "A LOT OF MONEY",
            "team_id": 1
    },
    "success": true
}
```

#### GET /teams
- Requires authentication.
- Returns a list of all teams in the database.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.
    - Sample usage: `curl http://localhost:5000/teams -H 'Authorization: Bearer (insert bearer token here)'`
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
     ]
}
```

#### GET /teams/<int:team_id/details
- Requires authentication.
- Returns one teams specific details, which includes team total_payroll.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.
    - Sample usage: `curl http://localhost:5000/teams -H 'Authorization: Bearer (insert bearer token here)'`
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

#### GET /teams/<int:team_id/roster
- Requires authentication.
- Returns a team's complete player roster.
- The endpoint will return a status code of 200 if successful, or 404 if no players are found.
    - Sample usage: `curl http://localhost:5000/teams/1/roster -H 'Authorization: Bearer (insert bearer token here)'`
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