import click

from issue_fetcher.service import fetcher_tickets


@click.command()
def cli():
    """Fetch Fedora tickets"""
    result = fetcher_tickets.fetch_bugs()
    for bug in result:
        print(bug.summary)
    # print(result)
    print(len(result))
