# Apps

Methods:

- <code title="get /">client.apps.<a href="./src/identety/resources/apps.py">retrieve</a>() -> None</code>

# Clients

Types:

```python
from identety.types import Client, ClientListResponse
```

Methods:

- <code title="post /clients">client.clients.<a href="./src/identety/resources/clients.py">create</a>(\*\*<a href="src/identety/types/client_create_params.py">params</a>) -> <a href="./src/identety/types/client.py">Client</a></code>
- <code title="get /clients/{id}">client.clients.<a href="./src/identety/resources/clients.py">retrieve</a>(id) -> <a href="./src/identety/types/client.py">Client</a></code>
- <code title="patch /clients/{id}">client.clients.<a href="./src/identety/resources/clients.py">update</a>(id, \*\*<a href="src/identety/types/client_update_params.py">params</a>) -> <a href="./src/identety/types/client.py">Client</a></code>
- <code title="get /clients">client.clients.<a href="./src/identety/resources/clients.py">list</a>(\*\*<a href="src/identety/types/client_list_params.py">params</a>) -> <a href="./src/identety/types/client_list_response.py">ClientListResponse</a></code>
- <code title="delete /clients/{id}">client.clients.<a href="./src/identety/resources/clients.py">delete</a>(id) -> <a href="./src/identety/types/client.py">Client</a></code>

# Users

Methods:

- <code title="post /users">client.users.<a href="./src/identety/resources/users.py">create</a>(\*\*<a href="src/identety/types/user_create_params.py">params</a>) -> None</code>

# Orgs

Methods:

- <code title="get /org/{id}">client.orgs.<a href="./src/identety/resources/orgs.py">retrieve</a>(id) -> None</code>

# Roles

Methods:

- <code title="get /role/{id}">client.roles.<a href="./src/identety/resources/roles.py">retrieve</a>(id) -> None</code>
