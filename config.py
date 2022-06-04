import datetime


today_date = datetime.datetime.now()
month_before_today_date = today_date - datetime.timedelta(days=30)

DEFAULT_SINCE_DATE = month_before_today_date.strftime("%Y-%m-%d")           # date format is YYYY-MM-DD
DEFAULT_UNTIL_DATE = today_date.strftime("%Y-%m-%d")
DEFAULT_KEYWORD = "unretire"
API_RELENG_ISSUES_ENDPOINT = "https://pagure.io/api/0/releng/issues"
API_KEY = "XHJFGZL0C26V6FS9LK50VF8M6H2WIVSNYSCYZX555S8FVN8ODQ3RRXU1FNHEQ4S4"                 # your API KEY
RELENG_HEADERS = {"Authorization": f"token {API_KEY}"}

BUGZILLA_URL = "bugzilla.stage.redhat.com"
TICKET_LIMIT = 20
