from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Example scrape_jobs function (replace with your actual scraping logic)
def scrape_jobs(role):
    # For testing purposes, returning some sample job data based on role
    job_data = {
        'data-entry': [
            {"title": "Data Entry Clerk", "salary": "₹20,000", "location": "Mumbai"},
            {"title": "Data Entry Operator", "salary": "₹18,000", "location": "Pune"}
        ],
        'sales': [
            {"title": "Sales Manager", "salary": "₹30,000", "location": "Delhi"},
            {"title": "Sales Executive", "salary": "₹25,000", "location": "Bangalore"}
        ]
    }
    return job_data.get(role, [])

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Render the home page where roles are listed

# Dynamic route for job roles
@app.route('/jobs/<role>')
def jobs(role):
    # Fetch job data based on the role selected
    jobs_data = scrape_jobs(role)
    # Render job listing page for the selected role
    return render_template('jobs.html', role=role, jobs=jobs_data)

if __name__ == '__main__':
    app.run(debug=True)
