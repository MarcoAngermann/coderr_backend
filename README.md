# Coderr Offer Management System

## Overview
This project is a Django-based Offer Management System designed to facilitate the creation, retrieval, and management of offers, orders, and user profiles. It provides comprehensive backend functionality, including authentication, filtering, pagination, and validation.

## Features
- **Sales Page**: Displays all available offers.
- **Login and Registration**: Secure user authentication and registration system.
- **Offers Management**: Create, retrieve, update, and delete offers with detailed information.
- **User Profiles**:
  - Business and Customer profiles.
  - View own profile and profiles of others.
- **Orders Management**:
  - Track ongoing and completed orders.
  - Administrative tools for order management.
- **Reviews**:
  - Create and manage user reviews for business profiles.
- **Legal Pages**: Includes pages for Privacy Policy and Imprint.

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL or SQLite (for development purposes)
- Pipenv or virtualenv (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/offer-management-system.git
   cd offer-management-system
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  
   On Windows: env\Scriptsctivate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Offers
- **GET /offers/**: Retrieve a list of all offers (supports filtering and pagination).
- **POST /offers/**: Create a new offer.
- **GET /offers/{id}/**: Retrieve details of a specific offer.
- **PATCH /offers/{id}/**: Update details of a specific offer.
- **DELETE /offers/{id}/**: Delete an offer.
- **GET /offerdetails/{id}/**: Retrieve details of a specific offer detail.

### Orders
- **GET /orders/**: List orders for the logged-in user.
- **POST /orders/**: Create a new order based on an offer.
- **GET /orders/{id}/**: Retrieve details of a specific order.
- **PATCH /orders/{id}/**: Update the status of a specific order.
- **DELETE /orders/{id}/**: Delete an order (admin only).

### Reviews
- **GET /reviews/**: Retrieve a list of all reviews.
- **POST /reviews/**: Create a new review (authenticated users only).
- **GET /reviews/{id}/**: Retrieve details of a specific review.
- **PATCH /reviews/{id}/**: Update a review (owner or admin only).
- **DELETE /reviews/{id}/**: Delete a review (owner or admin only).

### User Profiles
- **GET /profile/{id}/**: Retrieve details of a user profile.
- **PATCH /profile/{id}/**: Update profile details (authenticated users only).
- **GET /profiles/business/**: Retrieve a list of all business profiles.
- **GET /profiles/customer/**: Retrieve a list of all customer profiles.

### Authentication
- **POST /login/**: Log in and retrieve an authentication token.
- **POST /registration/**: Register a new user.

### Miscellaneous
- **GET /base-info/**: Retrieve general platform statistics (e.g., number of reviews, average ratings).
