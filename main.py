import requests
import config

headers = {"Authorization": f"token {config.API_KEY}"}
params = {"status": "all",
          "per_page": 100}


def fetch_issues_between_dates():
    params["status"] = "Closed"
    date_since = input("Type date since you want to get issues in format 'YYYY-MM-DD' :")
    date_before = input("Type date before you want to get issues in format 'YYYY-MM-DD/tT' :")
    closed_issues_between = fetch_issues_since(date_since)
    if date_before.upper() != "T":
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


def fetch_issues_containing_keyword():
    title_keyword = input("Type your keyword (probably you want 'unretirement'): ")
    issues_containing_keyword = []
    response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
    pages_count = response.json()["pagination"]["pages"]
    issues_on_page = response.json()["issues"]
    issues_containing_keyword += [issue for issue in issues_on_page if title_keyword in issue["title"].lower()]
    if pages_count >= 2:
        for page in range(2, pages_count + 1):
            params["page"] = page
            response = requests.get(url=config.API_RELENG_ISSUES_ENDPOINT, headers=headers, params=params)
            issues_on_page = response.json()["issues"]
            issues_containing_keyword += [issue for issue in issues_on_page if title_keyword in issue["title"].lower()]
    return issues_containing_keyword


print("script is working")
IS_WORKING = True
while IS_WORKING:
    query = input("What do you want to fetch: \n"
                  "fetch issues between dates 'bd'\n"
                  "fetch issues that contain a keyword 'ck'\n"
                  "for exiting write 'q'\n"
                  "your choose: ")
    match query:
        case "bd":
            issues = fetch_issues_between_dates()
            print(issues)
        case "ck":
            issues = fetch_issues_containing_keyword()
            print(issues)
        case "q":
            IS_WORKING = False
        case _:
            print(f"You entered {query} its not correct!")
            continue
    desire_to_continue = input("Do you want to continue? 'yYnN': ")
    if desire_to_continue.lower() == "n":
        IS_WORKING = False

print("It's end!")