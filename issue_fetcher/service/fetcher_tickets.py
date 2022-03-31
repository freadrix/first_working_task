import bugzilla as bugzilla

from config import BUGZILLA_URL


def fetch_bugs():
    bzapi = bugzilla.Bugzilla(BUGZILLA_URL)
    bzapi.bug_autorefresh = True
    query = bzapi.build_query(
        product="Fedora",
        limit=None
    )
    bugs = bzapi.query(query)
    return bugs
