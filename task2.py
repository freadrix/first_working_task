import requests
from issue_fetcher.service.fetcher_issues import Fetcher
import git
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import shutil
from test_issues_data import test_issues_data
from unittest import mock
import time  # For compare two fetching methods


class Issue:
    """ A class used to contain info about single issue and work with this """

    def __init__(self, issue_name, user_name):
        self.issue_name = issue_name
        self.package_name = None
        self.user_name = user_name
        self.is_packager = None
        self.git_url = None
        self.last_commit_date = None

    def package_name_analyze(self):
        """ Method will analyze a package_name write down correct names and return bool value of name correctness """
        self.skip_unnecessary_symbols()
        self.get_package_name()

    def skip_unnecessary_symbols(self):
        skips = [".", ", ", ":", ";", "'", '"']
        for ch in skips:
            self.issue_name = self.issue_name.replace(ch, "")

    def get_package_name(self):
        package_prefixes = ("rpms/", "flatpaks/", "modules/", "tests/", "container/")
        text_with_package_name = self.issue_name.split("unretire ")[1] if "unretire" in self.issue_name \
            else self.issue_name.split("stalled epel package ")[1]
        list_of_issue_name_words = text_with_package_name.split(" ")
        for word in list_of_issue_name_words:
            if word.startswith(package_prefixes):
                package_name = word
                if self.get_git_url(package_name=package_name):
                    self.package_name = package_name
                    return True
            else:
                package_name = word
                if self.try_package_name_with_different_prefix(package_name=package_name,
                                                               package_prefixes=package_prefixes):
                    return True
        return False

    def try_package_name_with_different_prefix(self, package_name, package_prefixes):
        for prefix in package_prefixes:
            package_name_with_prefix = prefix + package_name
            if self.get_git_url(package_name=package_name_with_prefix):
                self.package_name = package_name_with_prefix
                return True
        return False

    def get_git_url(self, package_name):
        """ Method will fill git_url attr """
        git_url = "https://src.fedoraproject.org/" + package_name + ".git"
        if self.is_package_url_exist(git_url):
            self.git_url = git_url
            return True
        else:
            return False

    @staticmethod
    def is_package_url_exist(git_url):
        response = requests.get(git_url)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_last_commit_date_using_scraping(self):
        """ Method will fill last_commit_date attr """
        # Getting last commit
        g = git.cmd.Git()
        remote_branches_list = g.ls_remote(self.git_url).split("\n")
        head_branch = remote_branches_list[0]
        head_commit_hash = head_branch.split("\t")[0]
        last_commit_url = self.git_url.removesuffix(".git") + "/c/" + head_commit_hash

        # Scrapping last commit date
        page = urlopen(last_commit_url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all("span")
        span_with_last_commit_date = spans[16]  # 16 is nubmer of span that contain date of last commit in title
        last_commit_date = span_with_last_commit_date["title"]
        self.last_commit_date = last_commit_date

    def get_last_commit_date_using_git_clone(self):
        """ Method will fill last_commit_date attr """
        if Path("repo/").is_dir():
            shutil.rmtree("repo/")
        local_repo_dir = Path("repo/")
        repo = git.Repo.clone_from(self.git_url, local_repo_dir, depth=1)
        last_commit = repo.head.commit
        last_commit_date = last_commit.committed_datetime
        self.last_commit_date = last_commit_date


class Issues:
    """ A class used to contain and work with list of issue objects """

    def __init__(self):
        self.issues = []

    def get_unretire_issues(self):
        """ Method fetch issues that contain the unretire keyword in title """
        issue_fetcher = Fetcher(keyword="unretire")
        issues_contain_unretire_keyword_in_title = issue_fetcher.containing_keyword()
        for issue in issues_contain_unretire_keyword_in_title:
            issue_name = issue["title"].lower()  # .split("Unretire ")[1]
            user_name = issue["user"]["name"]
            issue_obj = Issue(issue_name=issue_name, user_name=user_name)
            self.issues.append(issue_obj)

    def get_stalled_epel_package_issues(self):
        """ Method fetch issues that contain the stalled epel package phrase in title """
        issue_fetcher = Fetcher(keyword="stalled epel package")
        issues_contain_stalled_epel_package_string_in_title = issue_fetcher.containing_keyword()
        for issue in issues_contain_stalled_epel_package_string_in_title:
            issue_name = issue["title"].lower()  # .split(": ")[1]
            user_name = issue["user"]["name"]
            issue_obj = Issue(issue_name=issue_name, user_name=user_name)
            self.issues.append(issue_obj)

    def analyze_name_issues(self):
        """ Method hard analyze each issue_name of issue in the list """
        # self.issues = [issue for issue in self.issues if issue.package_name is not None]
        new_issues_list = []
        for issue in self.issues:
            issue.package_name_analyze()
            if issue.package_name is not None:
                new_issues_list.append(issue)
        self.issues = new_issues_list

    def fill_last_commit_date_of_issues(self):
        """ Method fill last_commit_date attr in all issues """
        # Time using scraping for 3 packages is  : 3.833085775375366 seconds
        # Time using git clone for 3 packages is : 3.5828120708465576 seconds
        # start_time = time.time()
        for issue in self.issues:
            issue.get_last_commit_date_using_git_clone()
        # print("--- %s seconds ---" % (time.time() - start_time))

    def write_out_issues(self):
        """ Method writes out info about containing issues """
        print("List of issues:")
        for issue in self.issues:
            print(f"\tissue name is: {issue.issue_name}\n"
                  f"\tpackage name is: {issue.package_name}\n"
                  f"\tgit_url: {issue.git_url}\n"
                  f"\tuser name is : {issue.user_name}\n"
                  f"\tuser is packager : {issue.is_packager}\n"
                  f"\tlast commit date : {issue.last_commit_date}\n"
                  f"-----------------------------------------------------------------")


def main():
    issues = Issues()
    issues.get_unretire_issues()
    issues.get_stalled_epel_package_issues()
    issues.write_out_issues()
    issues.analyze_name_issues()
    issues.fill_last_commit_date_of_issues()
    issues.write_out_issues()
    # TODO make kerberos authentication             ✓
    # TODO analyze package name                     ✓
    # TODO found last commit date                   ✓
    # TODO found packager group at the user group
    # TODO create a test environment
    # TODO create a good text analyze               ✓


if __name__ == "__main__":
    main()
