import requests
import os
def trigger_dbt():
    headers =  {
        "Authorization": f"Token {os.getenv('DBT_AUTH_TOKEN')}"
    }
    account_id = int(os.getenv("DBT_ACCOUNT_ID")) #70403103918735
    job_id = int(os.getenv("DBT_JOB_ID")) #70403103919936
    body = {
    "cause": "Triggered via API",
    }
    response = requests.post(f"https://ok531.us1.dbt.com/api/v2/accounts/{account_id}/jobs/{job_id}/run/",  headers=headers, json=body)
    print(response)

