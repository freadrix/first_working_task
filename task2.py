from issue_fetcher.service.fetcher_issues import Fetcher


def main():
    issue_fetcher = Fetcher()
    issue_fetcher2 = Fetcher(keyword="stalled epel package")
    issues_after_parse = []

    issues_contain_unretire_keyword_in_title = issue_fetcher.containing_keyword()
    # print(issues_contain_unretire_keyword)

    # issues contain "unretire" in title
    for issue in issues_contain_unretire_keyword_in_title:
        package_name = issue["title"].split("Unretire ")[1]
        user_name = issue["user"]["name"]
        issue_dict = {
            "package_name": package_name,
            "user_name": user_name
        }
        issues_after_parse.append(issue_dict)

    issues_contain_stalled_epel_package_string_in_title = issue_fetcher2.containing_keyword()
    # print(issues_contain_stalled_epel_package_string_in_title)

    # issues contain "stalled epel package" in title
    for issue in issues_contain_stalled_epel_package_string_in_title:
        package_name = issue["title"].split(": ")[1]
        user_name = issue["user"]["name"]
        issue_dict = {
            "package_name": package_name,
            "user_name": user_name
        }
        issues_after_parse.append(issue_dict)

    print(issues_after_parse)


if __name__ == "__main__":
    main()
