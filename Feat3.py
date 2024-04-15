#This feature allows for the retrieval of job postings from the Adzuna API. The user can specify the job title and location to search for job postings.

import requests

def retrieve_job_postings(app_id, app_key, what, where):
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": what,
        "where": where,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return None

data = retrieve_job_postings('<YourAPPId>', '<YourAPIkey>', 'python', 'london')

if data and 'results' in data:
    for job in data['results']:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']['display_name']}")
        print(f"Location: {job['location']['display_name']}")
        print(f"URL: {job['redirect_url']}")
        print(f"Description: {job['description']}")
        print("\n")
