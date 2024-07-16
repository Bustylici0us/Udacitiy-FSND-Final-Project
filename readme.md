Project Documentation
Motivation
In the rapidly evolving world of digital media, the need for a streamlined, secure, and efficient way to manage film production processes has never been more critical. This project aims to address these needs by providing a comprehensive solution that facilitates the management of movies and actors, streamlining the casting process, and enhancing collaboration among different roles within a production team. By leveraging modern technologies and best practices in security and deployment, this project ensures a seamless, user-friendly experience for casting assistants, directors, and executive producers alike.

Environmental Variables
The application relies on several environmental variables to configure its behavior and integrate with external services. Below is a list of these variables and their significance:

CASTING_ASSISTANT_TOKEN: A JWT token used to authenticate a user with the role of a Casting Assistant. This role has permissions to view actors and movies.

CASTING_DIRECTOR_TOKEN: A JWT token for authenticating a user with the role of a Casting Director. This role extends the permissions of a Casting Assistant by allowing the addition or deletion of an actor from the database and modifying actors or movies.

EXECUTIVE_PRODUCER_TOKEN: A JWT token designated for users with the Executive Producer role. This role has all the permissions of a Casting Director, with the added ability to add or delete a movie from the database.

AUTH0_DOMAIN: The domain of the Auth0 application, used for secure authentication and authorization services.

AUTH0_CLIENT_ID: The client ID for the Auth0 application, necessary for the app to identify itself to Auth0.

AUTH0_CLIENT_SECRET: A secret key used by the application to authenticate with Auth0 securely. It should be kept confidential.

SERVER_URL: The URL where the application is hosted. This is used for various callbacks and by the frontend to communicate with the backend.

DATABASE_NAME: The name of the database where the application's data is stored. This is crucial for connecting to the database and performing operations.
Security and Deployment
This project uses Auth0 for secure login and authentication. Auth0 provides robust, easy-to-implement authentication and authorization services, ensuring that only authorized users can access certain functionalities based on their roles.

For deployment, Render is our platform of choice. Render offers seamless deployment options, ensuring our application is always available and scalable according to demand. This combination of Auth0 for security and Render for deployment guarantees that our application is not only secure but also highly available and performant.

Application Structure
This application is structured around three main scripts, each serving a distinct purpose in the overall functionality of the project. Additionally, the project dependencies are managed through a requirements.txt file, ensuring easy setup and consistent environments across different setups.

Scripts
models.py: This script defines the database models for the application. It outlines the schema for movies and actors, facilitating interactions with the database for CRUD operations.

authorization.py: Handles authentication and authorization logic. It integrates with Auth0 to secure endpoints and ensure that users have the appropriate permissions to perform certain actions.

app.py: The core of the application, where the Flask application is defined and routes are set up. It serves as the entry point for the application, tying together the models and authorization logic to provide a cohesive API.

Dependency Management
requirements.txt: Lists all the necessary Python packages required to run the application. This file is crucial for setting up a development environment or deploying the application, as it ensures that all dependencies are installed and at the correct versions. To install these dependencies, one would typically run pip install -r requirements.txt in their terminal.
This structure ensures that the application is modular, with clear separation of concerns, making it easier to maintain and extend. The use of requirements.txt for managing dependencies further simplifies setup and deployment processes.



The models.py file defines the database setup and models for a Flask application that manages movies and actors. Here's a breakdown of its components:

Database Configuration:

Imports SQLAlchemy and os for database management and environment variable access.
Retrieves the database path from an environment variable DATABASE_NAME.
Initializes a SQLAlchemy object db.
Database Setup Functions:

setup_db(app, database_path=database_path): Configures the Flask app to use SQLAlchemy with the given database path. It also disables track modifications for performance reasons.
db_drop_and_create_all(): Drops all tables and recreates them. This is useful for resetting the database to a clean state.

Movie Model:

Defines a Movie model with id, title, and release_date fields.
Includes methods for inserting, updating, deleting, and formatting movie instances for JSON responses.
Actor Model:

Defines an Actor model with id, name, age, and gender fields.
Includes methods for inserting, updating, deleting, and formatting actor instances for JSON responses.
This setup allows the Flask application to interact with a database for CRUD operations on movies and actors, providing a structured way to manage data for the application's endpoints.


The authorization.py  is a module for handling authentication and authorization in a Flask application, using Auth0 as the authentication provider. It defines a custom AuthError exception, functions for extracting and verifying JWT tokens from the Authorization header, checking permissions, and a decorator for protecting routes that require authentication. Here's a breakdown of its components:

Imports and Global Variables:

Imports necessary modules and functions.
Retrieves Auth0 domain and audience from environment variables and sets the algorithm used for JWT tokens.
AuthError Class:

A custom exception class for handling authentication errors, with an error message and status code.
handle_auth_error Function:

A function to format and return error responses when an AuthError is raised.
get_token_auth_header Function:

Extracts the JWT token from the Authorization header of the request.
Validates the format of the Authorization header and returns the token if valid.
check_permissions Function:

Checks if the JWT token payload contains the required permission.
Raises an AuthError if the permission is not present.
verify_decode_jwt Function:

Verifies the JWT token using Auth0's public keys.
Decodes the JWT token and validates its claims (expiration, audience, issuer).
Returns 

THe app.py sets up a REST API for managing movies and actors. Here's a breakdown of its components and functionalities:

Imports and Setup:

Imports necessary modules and functions (Flask, request, jsonify, abort, setup_db, Movie, Actor, db_drop_and_create_all, CORS, requires_auth).
Initializes the Flask app, sets up the database, and applies CORS.
Database Initialization:

With the application context, it drops existing tables and creates new ones to start with a clean state.
Routes and Endpoints:

GET /movies: Fetches a list of movies. Requires get:movies permission.
GET /actors: Fetches a list of actors. Requires get:actors permission.
POST /movies: Creates a new movie. Requires post:movies permission. It expects a JSON body with title and release_date.
POST /actors: Creates a new actor. Requires post:actors permission. It expects a JSON body with name, age, and gender.
PATCH /movies/<movie_id>: Updates an existing movie identified by movie_id. Requires patch:movies permission. It can update title and/or release_date.
PATCH /actors/<actor_id>: Updates an existing actor identified by actor_id. Requires patch:actors permission. It can update name, age, and/or gender.
DELETE /movies/<movie_id>: Deletes a movie identified by movie_id. Requires delete:movies permission.
DELETE /actors/<actor_id>: Deletes an actor identified by actor_id. Requires delete:actors permission.
Authorization:

Each route is protected with the requires_auth decorator, which checks for the required permission in the JWT token provided by the client.
Error Handling:

Uses abort(400) for bad requests (e.g., missing required fields in the request body) and abort(404) for not found resources (e.g., trying to update or delete a non-existing movie or actor).
Running the Application:

The application is configured to run with app.run() if executed as the main program.
This application provides a comprehensive API for managing a database of movies and actors, with role-based access control for different operations.
