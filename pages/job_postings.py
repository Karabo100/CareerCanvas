#This feature allows for the retrieval of job postings from the Adzuna API. The user can specify the job title and location to search for job postings.

import streamlit as st
import requests

def retrieve_job_postings(what, where):
    #Adzuna API credentials
    app_key = "656f9aee07b49a0114dc1d5281a6f72e"
    api_id = "d547cbe3"
    url = "http://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": api_id,
        "app_key": app_key,
        "what": what,
        "where": where,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve job postings. Status code: {response.status_code}")
        st.error(f"Response text: {response.text}")
        return None

def job_postings():
    st.title("Job Postings")
    st.write("This feature allows for the retrieval of job postings from the Adzuna API. The user can specify the job title and location to search for job postings.")

    #app_id = st.text_input("Enter your Adzuna App ID:")
    #app_key = st.text_input("Enter your Adzuna API Key:")
    what = st.text_input("Enter job title (e.g., financial analyst):")
    where = st.text_input("Enter location (e.g., london):")

    if st.button("Retrieve Job Postings"):
        data = retrieve_job_postings(what, where)
        if data and 'results' in data:
            for job in data['results']:
                st.write(f"Title: {job['title']}")
                st.write(f"Company: {job['company']['display_name']}")
                st.write(f"Location: {job['location']['display_name']}")
                st.write(f"URL: {job['redirect_url']}")
                st.write(f"Description: {job['description']}")
                st.write("---")

if __name__ == "__main__":
    job_postings()

