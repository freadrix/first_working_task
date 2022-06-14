import sys

import requests

from config import DEFAULT_UNTIL_DATE, DEFAULT_SINCE_DATE, DEFAULT_KEYWORD, RELENG_HEADERS, API_RELENG_ISSUES_ENDPOINT


class Fetcher:

    def __init__(self, date_since=None, date_until=None, keyword=None):
        self.params = {"status": "all",
                       "per_page": 100}
        self.date_since = date_since or DEFAULT_SINCE_DATE
        self.date_until = date_until or DEFAULT_UNTIL_DATE
        self.keyword = keyword

    def between_dates(self):
        self.params["status"] = "Closed"
        closed_issues_between = self.issues_since(self.date_since)
        closed_before = self.issues_since(self.date_until)
        for issue in closed_before:
            if issue in closed_issues_between:
                closed_issues_between.remove(issue)
        return closed_issues_between

    def issues_since(self, date):
        self.params["since"] = date
        response = requests.get(url=API_RELENG_ISSUES_ENDPOINT, headers=RELENG_HEADERS, params=self.params)
        closed_issues_since = response.json()["issues"]
        pages_count = response.json()["pagination"]["pages"]
        if pages_count > 1:
            for page in range(2, pages_count + 1):
                self.params["page"] = page
                response = requests.get(url=API_RELENG_ISSUES_ENDPOINT, headers=RELENG_HEADERS, params=self.params)
                closed_issues_since += response.json()["issues"]
        return closed_issues_since

    def containing_keyword(self):
        # <<<<<<<< 2. Task version
        if self.is_keyword_none():
            sys.exit("keyword is none")
        else:
            self.params["status"] = "Open"
            print(self.keyword)
            # >>>>>>>> Old version
            issues_containing_keyword = []
            response = requests.get(url=API_RELENG_ISSUES_ENDPOINT, headers=RELENG_HEADERS, params=self.params)
            pages_count = response.json()["pagination"]["pages"]
            issues_on_page = response.json()["issues"]
            # print(type(issues_on_page))
            # print(issues_on_page)
            issues_containing_keyword += [issue for issue in issues_on_page if self.keyword in issue["title"].lower()]
            if pages_count >= 2:
                for page in range(2, pages_count + 1):
                    self.params["page"] = page
                    response = requests.get(url=API_RELENG_ISSUES_ENDPOINT, headers=RELENG_HEADERS, params=self.params)
                    issues_on_page = response.json()["issues"]
                    issues_containing_keyword += [issue for issue in issues_on_page if
                                                  self.keyword in issue["title"].lower()]
            return issues_containing_keyword

    def is_keyword_none(self):
        return self.keyword is None
