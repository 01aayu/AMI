import csv
from models.job import Job
from typing import List, Set


def is_complete_job(job: dict, required_keys: List[str]) -> bool:
    return all(key in job and job[key] for key in required_keys)

def is_duplicate_job(title: str, seen_titles: Set[str]) -> bool:
    return title.lower() in seen_titles

def save_venues_to_csv(venues: list, filename: str):
    if not venues:
        print("No venues to save.")
        return

    # Use field names from the Venue model
    fieldnames = Job.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} venues to '{filename}'.")
