# Email Scrapper
<img src="https://github.com/abrarbinrofique/Email-scrapper-/blob/main/mails.png">



Email Scrapper is a tool designed to extract emails from websites. The project is built using Django REST API for the backend and React.js for the frontend.

## Features

- **Email Extraction**: Scrapes emails from websites based on provided URLs.
- **Data Management**: Captures additional details like the website title and URL.
- **User Management**: Includes basic user management features.

## Technologies Used

### Backend
- ![Django REST Framework](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

### Frontend
- ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## Installation (Backend - Django)

1. Clone the repository:
    ```bash
    git clone git@github.com:abrarbinrofique/Email-scrapper-.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Email-scrapper-
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

## Installation (Frontend - React.js)

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Run the React development server:
    ```bash
    npm start
    ```

## Project Structure

- **Emailscrapper/**: Core app for handling the scraping logic.
- **scrapping/**: Handles the scraping processes and manages email data.
- **user/**: Manages user authentication and profile data.

## Requirements

The main dependencies (as listed in `requirements.txt`) are:

- Django
- djangorestframework
- psycopg2-binary (for PostgreSQL)
- requests
- and more...

## Usage

- Once both the Django and React servers are running, you can use the platform to input website URLs and start scraping emails.
- The results will show the extracted emails along with the website title and URL.


