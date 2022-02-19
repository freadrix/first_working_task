import requests
import config

headers = {"Authorization": f"token {config.API_KEY}"}
params = {"status": "all",
          "per_page": 100}


def fetch_issues_between_dates(first_date, second_date):
    pass


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


unretirement_issues = fetch_unretirement_issues()


# response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)

# print(response.json())
# issues = response.json()["issues"]
# print(issues[0])

# closed_issues = [issue for issue in issues if issue["status"] == "Closed"]
#
# print(len(closed_issues))
