import requests
import config

headers = {"Authorization": f"token {config.API_KEY}"}
params = {"status": "all",
          "per_page": 100}


def fetch_issues_between_dates():  # here must be two parameters first_date, second_date
    params["status"] = "Closed"
    date_since = input("Type date since you want to get issues in format 'YYYY-MM-DD' :")
    date_before = input("Type date before you want to get issues in format 'YYYY-MM-DD' :")
    closed_issues_between = fetch_issues_since(date_since)
    closed_before = fetch_issues_since(date_before)
    for issue in closed_before:
        if issue in closed_issues_between:
            closed_issues_between.remove(issue)
    return closed_issues_between


def fetch_issues_since(date):
    params["since"] = date
    response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
    closed_issues_since = response.json()["issues"]
    pages_count = response.json()["pagination"]["pages"]
    if pages_count > 1:
        for page in range(2, pages_count + 1):
            params["page"] = page
            response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
            closed_issues_since += response.json()["issues"]
    return closed_issues_since


def fetch_unretirement_issues():
    title_keyword = "unretirement"
    unretirement_issues = []
    response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
    pages_count = response.json()["pagination"]["pages"]
    issues = response.json()["issues"]
    unretirement_issues += [issue for issue in issues if title_keyword in issue["title"].lower()]
    if pages_count >= 2:
        for page in range(2, pages_count + 1):
            params["page"] = page
            response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
            issues = response.json()["issues"]
            unretirement_issues += [issue for issue in issues if title_keyword in issue["title"].lower()]
    return unretirement_issues


closed_issues = fetch_issues_between_dates()
print(closed_issues)
# unretirement_issues = fetch_unretirement_issues()
