import datetime


today_date = datetime.datetime.now()
month_before_today_date = today_date - datetime.timedelta(days=30)

DEFAULT_SINCE_DATE = today_date.strftime("%Y-%m-%d")           # date format is YYYY-MM-DD
DEFAULT_UNTIL_DATE = month_before_today_date.strftime("%Y-%m-%d")
DEFAULT_KEYWORD = "unretirement"
API_RELENG_ISSUES_ENDPOINT = "https://pagure.io/api/0/releng/issues"
API_KEY = "<your_api_key>"                 # your API KEY