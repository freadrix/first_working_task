import bugzilla as bugzilla

from config import BUGZILLA_URL, TICKET_LIMIT


def fetch_bugs():
    bzapi = bugzilla.Bugzilla(BUGZILLA_URL)
    bzapi.bug_autorefresh = True
    query = bzapi.build_query(
        product="Fedora",
        limit=TICKET_LIMIT                      # automatic limit cannot change it
    )
    bugs = bzapi.query(query)

    for i in range(1, 10):                      # Cycle for getting 200 bugs instead of 20
        query['offset'] = i * TICKET_LIMIT
        bugs += bzapi.query(query)

    return bugs
