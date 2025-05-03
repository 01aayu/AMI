from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient("mongodb+srv://AMI:1234@aayushcluster.mvfntk6.mongodb.net/")  # Replace with your MongoDB connection string
db = client['jobs']  # Replace with your database name
job_collection = db['jobsDB']  # Replace with the name of your collection

# Example scrape_jobs function (replace with your actual scraping logic)
def scrape_jobs(role):
    # For testing purposes, returning some sample job data based on role
    job_data = {
        'data-entry': [
            {"title": "Data Entry Clerk", "salary": "₹20,000", "location": "Mumbai"},
            {"title": "Data Entry Operator", "salary": "₹18,000", "location": "Pune"}
        ],
        'Sales': [
            {"title": "Sales Manager", "salary": "₹30,000", "location": "Delhi"},
            {"title": "Sales Executive", "salary": "₹25,000", "location": "Bangalore"}
        ],
        'BPO': [
             {"title": "Customer Service Executive", "salary": "₹18,000", "location": "Noida"},
             {"title": "BPO Telecaller", "salary": "₹16,000", "location": "Mumbai"},
             {"title": "Telemarketing Executive", "salary": "₹17,500", "location": "Pune"},
            {"title": "BPO Team Leader", "salary": "₹30,000", "location": "Gurgaon"}
       ],
        'Delivery': [
            {"title": "Delivery Executive", "salary": "₹15,000", "location": "Bangalore"},
            {"title": "Bike Delivery Boy", "salary": "₹14,000", "location": "Chennai"},
            {"title": "Courier Delivery Person", "salary": "₹13,500", "location": "Mumbai"},
            {"title": "Delivery Manager", "salary": "₹30,000", "location": "Delhi"}
        ],
        'Helper': [
            {"title": "Office Helper", "salary": "₹12,000", "location": "Hyderabad"},
            {"title": "Household Helper", "salary": "₹10,500", "location": "Bangalore"},
            {"title": "Office Assistant", "salary": "₹13,000", "location": "Pune"},
            {"title": "Office Helper (Part-time)", "salary": "₹8,000", "location": "Mumbai"}
        ],
        'Driver': [
            {"title": "Private Driver", "salary": "₹20,000", "location": "Delhi"},
            {"title": "Taxi Driver", "salary": "₹18,500", "location": "Mumbai"},
            {"title": "Delivery Driver", "salary": "₹15,500", "location": "Bangalore"},
            {"title": "Bus Driver", "salary": "₹25,000", "location": "Chennai"}
        ],
        'Teacher': [
            {"title": "Primary School Teacher", "salary": "₹22,000", "location": "Delhi"},
            {"title": "High School Teacher", "salary": "₹25,000", "location": "Bangalore"},
            {"title": "English Teacher", "salary": "₹20,000", "location": "Pune"},
            {"title": "Private Tutor", "salary": "₹18,000", "location": "Mumbai"}
        ],
        'Guard': [
            {"title": "Security Guard", "salary": "₹12,000", "location": "Mumbai"},
            {"title": "Night Security Guard", "salary": "₹14,000", "location": "Delhi"},
            {"title": "Security Supervisor", "salary": "₹20,000", "location": "Bangalore"},
            {"title": "Residential Security Guard", "salary": "₹10,500", "location": "Chennai"}
        ],
        'Receptionist': [
            {"title": "Front Desk Receptionist", "salary": "₹18,000", "location": "Delhi"},
            {"title": "Office Receptionist", "salary": "₹15,500", "location": "Mumbai"},
            {"title": "Hotel Receptionist", "salary": "₹16,000", "location": "Bangalore"},
            {"title": "Corporate Receptionist", "salary": "₹20,000", "location": "Chennai"}
        ],
        'Electrician': [
            {"title": "Electrician", "salary": "₹20,000", "location": "Mumbai"},
            {"title": "Electrical Technician", "salary": "₹18,500", "location": "Delhi"},
            {"title": "Electrician Helper", "salary": "₹15,000", "location": "Chennai"},
            {"title": "Industrial Electrician", "salary": "₹30,000", "location": "Bangalore"}
        ],
        'Nurse': [
            {"title": "Nurse", "salary": "₹25,000", "location": "Delhi"},
            {"title": "Staff Nurse", "salary": "₹22,000", "location": "Mumbai"},
            {"title": "Nursing Assistant", "salary": "₹20,000", "location": "Bangalore"},
            {"title": "Critical Care Nurse", "salary": "₹35,000", "location": "Chennai"}
        ],
        'Beautician': [
            {"title": "Beautician", "salary": "₹15,000", "location": "Mumbai"},
            {"title": "Hair Stylist", "salary": "₹18,000", "location": "Delhi"},
            {"title": "Makeup Artist", "salary": "₹20,000", "location": "Bangalore"},
            {"title": "Beauty Consultant", "salary": "₹22,000", "location": "Chennai"}
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

# MySQL connection


@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    return render_template('post_job.html')

if __name__ == '__main__':
    app.run(debug=True)
