# App

Methods:

- <code title="get /">client.app.<a href="./src/identety/resources/app.py">retrieve</a>() -> None</code>

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

Types:

```python
from identety.types import User, UserListResponse
```

Methods:

- <code title="post /users">client.users.<a href="./src/identety/resources/users.py">create</a>(\*\*<a href="src/identety/types/user_create_params.py">params</a>) -> <a href="./src/identety/types/user.py">User</a></code>
- <code title="get /users/{id}">client.users.<a href="./src/identety/resources/users.py">retrieve</a>(id) -> <a href="./src/identety/types/user.py">User</a></code>
- <code title="put /users/{id}">client.users.<a href="./src/identety/resources/users.py">update</a>(id, \*\*<a href="src/identety/types/user_update_params.py">params</a>) -> <a href="./src/identety/types/user.py">User</a></code>
- <code title="get /users">client.users.<a href="./src/identety/resources/users.py">list</a>(\*\*<a href="src/identety/types/user_list_params.py">params</a>) -> <a href="./src/identety/types/user_list_response.py">UserListResponse</a></code>
- <code title="delete /users/{id}">client.users.<a href="./src/identety/resources/users.py">delete</a>(id) -> <a href="./src/identety/types/user.py">User</a></code>

# Orgs

Methods:

- <code title="get /org/{id}">client.orgs.<a href="./src/identety/resources/orgs.py">retrieve</a>(id) -> None</code>

# Roles

Methods:

- <code title="get /role/{id}">client.roles.<a href="./src/identety/resources/roles.py">retrieve</a>(id) -> None</code>
