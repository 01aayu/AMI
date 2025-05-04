from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    job_type: str
    description: str
    posted_date: str
