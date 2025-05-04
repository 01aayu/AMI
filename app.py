from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os, json, logging

app = Flask(__name__)

load_dotenv()  # loads from .env by default

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)  # Replace with your MongoDB connection string
db = client['jobs_db']  # Replace with your database name
job_collection = db['job_seeker']  # Replace with the name of your collection

# Configure logging (optional, but VERY helpful for debugging)
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG (or INFO)
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Render the home page where roles are listed

@app.route('/jobs', methods=['GET'])
def jobs():
    role_filter = request.args.get('role', '').strip()
    location_filter = request.args.get('location', '').strip()
    job_type_filter = request.args.get('job_type', '').strip()
    min_salary = request.args.get('min_salary', '').strip()

    filename = f'data/{role_filter.replace(" ", "_")}_jobs.json' if role_filter else 'data/all_jobs.json'

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)
    else:
        jobs_data = []

    filtered_jobs = []
    for job in jobs_data:
        if role_filter and role_filter.lower() not in job.get('title', '').lower():
            continue
        if location_filter and location_filter.lower() not in job.get('location', '').lower():
            continue
        if job_type_filter and job_type_filter.lower() != job.get('job_type', '').lower():
            continue
        if min_salary:
            try:
                salary = job.get('salary', '').replace(',', '').replace('₹', '')
                job_salary = int(salary.split('-')[0].strip())
                if job_salary < int(min_salary):
                    continue
            except:
                continue
        filtered_jobs.append(job)

    return render_template("jobs.html", jobs=filtered_jobs, role=role_filter, request=request)

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_data = {
            "title": request.form.get("title"),
            "job_type": request.form.getlist("job_type"),  # checkbox input
            "role": request.form.get("role"),
            "salary_min": request.form.get("salary_min"),
            "salary_max": request.form.get("salary_max"),
            "experience_min": request.form.get("experience_min"),
            "experience_max": request.form.get("experience_max"),
            "city": request.form.get("city"),
            "localities": request.form.get("localities"),
            "description": request.form.get("description"),
        }

        job_collection.insert_one(job_data)
        return redirect(url_for('home'))  # or show success message

    return render_template('post_job.html')

@app.route('/search')
def search():
    """
    Handles the search request and displays job results using Apriori.
    """
    logger.debug("Search route accessed")
    query = request.args.get('keyword', '')
    logger.debug(f"Search query: {query}")

    df = load_job_data()
    if df is None:
        return render_template('search.html', keyword=query, jobs_data=[])

    df_encoded = preprocess_data(df)
    keywords = extract_keywords(query)
    jobs_data = find_associated_jobs(df_encoded, keywords, df)

    logger.debug(f"Rendering search.html with {len(jobs_data)} jobs")
    return render_template('search.html', keyword=query, jobs_data=jobs_data)

@app.route('/login')
def login():
    logger.debug("Login route accessed")
    return render_template('auth.html', form_type='login')

@app.route('/register')
def register():
    logger.debug("Register route accessed")
    return render_template('auth.html', form_type='register')

def check_credentials(email, password):
    """
    Checks if the provided email and password match a user in the database.
    Uses bcrypt for password verification.
    """
    logger.debug(f"Checking credentials for email: {email}")
    user = user_collection.find_one({'email': email})  # Find user by email
    if user:
        logger.debug(f"User found in database: {user['email']}")
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # If user exists and password matches
            logger.info("Login successful (password matched)")
            session['user_id'] = str(user['_id'])  # Store user ID in the session
            session['user_name'] = user['name']  # store the user name
            return True
        else:
            logger.warning("Login failed: Password did not match")
            return False
    else:
        logger.warning("Login failed: User not found")
        return False


def create_user(name, email, password):
    """
    Creates a new user in the database with the provided information.
    Hashes the password using bcrypt before storing it.
    """
    logger.debug(f"Creating user: name={name}, email={email}")
    if user_collection.find_one({'email': email}):
        logger.warning(f"Email already exists: {email}")
        return False  # Email already exists
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(
        'utf-8'
    )  # Hash the password
    user_data = {
        'name': name,
        'email': email,
        'password': hashed_password,
    }
    try:
        user_id = user_collection.insert_one(user_data).inserted_id
        session['user_id'] = str(user_id)  # Store the new user's ID in the session
        session['user_name'] = name  # store user name
        logger.info(f"User created successfully: {email}, id={user_id}")
        return True
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False

@app.route('/login', methods=['POST'])
def handle_login():
    logger.debug("Handling login POST request")
    email = request.form['email']
    password = request.form['password']
    logger.debug(f"Email from form: {email}, password from form: {password}")
    if check_credentials(email, password):
        logger.info("Login successful, redirecting to home")
        return redirect(url_for('home'))  # Redirect to the home page
    else:
        logger.warning("Login failed")
        return render_template('auth.html', form_type='login', error='Invalid credentials')

@app.route('/register', methods=['POST'])
def handle_register():
    logger.debug("Handling register POST request")
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    logger.debug(
        f"Name from form: {name}, email from form: {email}, password from form: {password}, confirm_password: {confirm_password}")

    if password != confirm_password:
        logger.warning("Passwords do not match")
        return render_template('auth.html', form_type='register', error='Passwords do not match')

    if create_user(name, email, password):
        logger.info("Registration successful, redirecting to login")
        return redirect(url_for('login'))  # Redirect to login
    else:
        logger.warning("Registration failed")
        return render_template('auth.html', form_type='register', error='Email already taken')

# New route for the employer form
@app.route('/form')
def employer_form():
    """Renders the employer form page (form.html)."""
    logger.debug("Employer form route accessed")
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
