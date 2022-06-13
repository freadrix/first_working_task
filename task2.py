import requests
from issue_fetcher.service.fetcher_issues import Fetcher
import git
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import shutil
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
        # First version
        # word_list = self.package_name.split()
        # count_of_words = len(word_list)
        # if count_of_words == 1:
        #     if self.package_name.startswith("rpms/"):
        #         return True
        #     else:
        #         self.package_name = f"rpms/{self.package_name}"
        #         return True
        # else:
        #     return False
        # Second version
        # package_versions = ["rpms/", "flatpaks/", "modules/"]
        # package_name_word_list = self.package_name.split()
        # for word in package_name_word_list:
        #     if self.package_name.startswith("rpms/"):
        #         print("True")
        #     else:
        #         self.package_name = f"rpms/{self.package_name}"
        #         print("True")

    def skip_unnecessary_symbols(self):
        skips = [".", ", ", ":", ";", "'", '"']
        for ch in skips:
            self.issue_name = self.issue_name.replace(ch, "")

    def get_git_url(self):
        """ Method will fill git_url attr """
        self.git_url = "https://src.fedoraproject.org/" + self.package_name + ".git"
        return self.is_package_url_exist()

    def is_package_url_exist(self):
        response = requests.get(self.git_url)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_last_commit_date_using_scraping(self):
        """ Method will fill last_commit_date attr """
        # Getting last commit
        self.get_git_url()
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
        self.get_git_url()
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
        self.issues = [issue for issue in self.issues if issue.package_name_analyze()]

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
                  f"\tuser name is : {issue.user_name}\n"
                  f"\tuser is packager : {issue.is_packager}\n"
                  f"\tlast commit date : {issue.last_commit_date}\n"
                  f"-----------------------------------------------------------------")


def main():
    issues = Issues()
    issues.get_unretire_issues()
    issues.get_stalled_epel_package_issues()
    issues.write_out_issues()
    # issues.analyze_name_issues()
    # issues.fill_last_commit_date_of_issues()
    # issues.write_out_issues()
    # TODO make kerberos authentication             ✓
    # TODO analyze package name                     ✓
    # TODO found last commit date                   ✓
    # TODO found packager group at the user group
    # TODO create a test environment
    # TODO create a good text analyze


if __name__ == "__main__":
    main()
