# Django REST API 

This project provides a Django REST API with CRUD (Create, Read, Update, Delete) operations for managing authors, books, and orders.

## Features

- Supports user registration.
- Implements token-based authentication.
- Provides endpoints for CRUD operations on authors, books, and orders.
- Includes pagination, filtering, and ordering for list views.

## Usage

### User Registration
- Endpoint: `/api/register/`
- Method: POST
- Description: Register a new user.
- Required fields: username, email, password.

### Token Generation (Login)
- Endpoint: `/api/token/`
- Method: POST
- Description: Generate an authentication token.
- Required fields: username, password.

### Authors
- Endpoint: `/api/authors/`
- Description: Get a list of authors or create a new author.
- Supported Methods: GET (List), POST (Create)

- Endpoint: `/api/authors/<pk>/`
- Description: Get, update, or delete an author.
- Supported Methods: GET (Retrieve), PUT (Update), DELETE (Delete)

### Books
- Endpoint: `/api/books/`
- Description: Get a list of books or create a new book.
- Supported Methods: GET (List), POST (Create)

- Endpoint: `/api/books/<pk>/`
- Description: Get, update, or delete a book.
- Supported Methods: GET (Retrieve), PUT (Update), DELETE (Delete)

### Orders
- Endpoint: `/api/orders/`
- Description: Get a list of orders.
- Supported Methods: GET (List)

- Endpoint: `/api/orders/create/`
- Description: Create a new order.
- Supported Methods: POST (Create)

- Endpoint: `/api/orders/callback/`
- Description: Handle order callbacks from external service.
- Supported Methods: POST (Create)

## API Documentation

Explore the API endpoints using Swagger: [Swagger Documentation](https://app.swaggerhub.com/apis-docs/VIKTSHNUIPT27/library-api/1.0.0#/)
