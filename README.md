# 1. Simple-Online-Store

## Wok Way Fried Rice Online Store
Simple online store front with CRUD functionalities for the purposes of editing and viewing fried rice dishes. 
- Backend API server implemented with: 
    - Flask for its application and endpoints 
    - SQLAlchemy for ORM 
    - Grahql for queries and mutations 
- Frontend is rendered using jinja2 web templating engine 
- Database makes use of a local SQLite3 database 

## Setup
### **Docker**
#### **Check Docker**
Ensure that Docker is installed and running on your machine

#### **Check controller.py**
Ensure that the `graphql_URL` configured in `controller.py` is the one configured for running via Docker:
```
graphql_URL = "http://gql_app:5001/graphql"
```
#### **Build Docker images**
In the root of the project folder where the `docker-compose.yml` file is, run 
```
docker-compose build
```

#### **Start Containers**
After the images have been built, run
```
docker-compose up
```

### **Security Measures Implemented**

#### **Input Validation**
1. Frontend HTML is generated with the use of jinja web templating engine as `.html.j2` files to escape HTML -> prevent arbitrary HTML and JS from being rendered in website's context (XSS by arbitrary HTML injection)
2. Input variables in forms are passed in double `{{value}}` quotes when processed and submitted as jinja expressions -> prevent (XSS by attribute injection)

#### **Logging**
1. In the backend both API controller Flask app and the Graphql interface app are run with the development server built-in debugger set to `Debug=False` -> This prevents arbitrary python code from being executed from the browser. 


### **Troubleshooting**
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5002 -> 0.0.0.0:0: listen tcp 0.0.0.0:5002: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
```

Run as administrator:
```
net stop winnat
net start winnat
```

## Completed Objectives
### Frontend Webpage
1. page to list all the items in the store
2. A form to add / update item in the store
3. Demonstrate calling API to perform CRUD

### Backend API Server
#### **Objectives**:
1. CRUD
    - CREATE an item in the store
    - READ list of all items in the store
    - UPDATE an item in the store
    - DELETE an item in the store
2. JSON response
3. Item attributes:
    - ID
    - Name
    - Price

### **Optional Objectives**
- Containerised backend and frontend via Docker
- Integrated database wrapper (ORM) via SQLAlchemy
