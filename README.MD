# Khoj - AI-Powered Blue-Collar Job Platform

*Khoj* is a web platform designed to streamline the process of finding blue-collar jobs, potentially focusing initially on areas like Navi Mumbai, Maharashtra, and expanding across India. It automates the aggregation of job listings from relevant sources using AI (Grok, Deepseek) and provides a user-friendly interface for job seekers to search, browse, and apply. The platform also includes features for employers/listers to post jobs directly.

## Problem Statement

Manually collecting job listings for the blue-collar sector from diverse sources like NSDC, Skill India, and Quikr is time-consuming, prone to errors, and results in a poor experience for job seekers who face overwhelming, unfiltered information. Khoj aims to solve this by automating data collection and providing a dedicated, easy-to-use platform tailored to this specific job market.

## Features

* *AI-Powered Scraping:* Automatically scrapes job data from external websites using Grok AI and Deepseek LLM APIs.
* *Structured Data:* Stores extracted job information in a structured format (JSON/Database).
* *Web Interface:* User-friendly frontend built with standard web technologies, served by a Flask backend.
* *Keyword Search:* Allows users to search for jobs using relevant keywords.
* *Role-Based Browse:* Enables filtering and Browse jobs based on predefined roles (e.g., Driver, Electrician, Data Entry). (As seen in UI)
* *Basic Recommendations:* Provides simple job suggestions based on user search keywords.
* *Manual Job Posting:* Allows registered employers/listers to post job openings directly.
* *User Authentication:* Includes user Login and Registration functionality. (As seen in UI)
* *Spotlight Ads:* Features prominent job listings on the main page. (As seen in UI)

## Tech Stack

* Backend: Python, Flask
* Frontend: HTML, CSS, JavaScript
* AI/LLM APIs: Grok AI API, Deepseek LLM API
* Database: PostgreSQL / MongoDB / SQLite (Choose one and specify)
* Data Format: JSON (for API communication and potentially initial storage)
* Libraries: Requests (for API calls), (mention others like SQLAlchemy/Flask-SQLAlchemy if used for DB, Flask-Login for auth, etc.)

## Architecture Overview

The system consists of three main parts:
1.  AI Scraping Module: A Python script/service that calls external LLM APIs (Grok, Deepseek) to fetch and structure job data from websites.
2.  Backend API: A Flask application that manages data in the database, handles user authentication, serves API endpoints for search, recommendations, and manual posting.
3.  Frontend Web Application: The user interface built with HTML/CSS/JS that interacts with the backend API to display information and capture user input.

*(You can optionally embed or link to the flowchart image ami.png here if included in your repository)*

## Setup and Installation

These are general steps. Adapt them based on your final project structure.

1.  *Clone the repository:*
    bash
    git clone <your-repository-link>
    cd khoj-project-directory
    

2.  *Create and activate a virtual environment:*
    bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    

3.  *Install dependencies:*
    bash
    pip install -r requirements.txt
    

4.  *Database Setup:*
    * Ensure your chosen database (e.g., PostgreSQL) is installed and running.
    * Configure the database connection string (see Configuration section).
    * Run database migrations if applicable (e.g., using Flask-Migrate):
        bash
        # flask db init  (if first time)
        # flask db migrate -m "Initial migration."
        # flask db upgrade
        

## Configuration

The application requires certain environment variables for configuration. Create a .env file in the root directory or set system environment variables:

# Flask Configuration
FLASK_APP=run.py # Or your main Flask app file
FLASK_ENV=development # Use 'production' for deployment
SECRET_KEY='your_strong_random_secret_key' # IMPORTANT: Change this!

# Database Configuration
DATABASE_URL='postgresql://user:password@host:port/dbname' # Example for PostgreSQL

# LLM API Keys
GROK_API_KEY='your_grok_api_key_here'
DEEPSEEK_API_KEY='your_deepseek_api_key_here'

## Demo

