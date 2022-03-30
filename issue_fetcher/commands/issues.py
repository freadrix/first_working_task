import click

from issue_fetcher.service import fetcher


class Context:
    def __init__(self, keyword, date_since, date_until):
        self.keyword = keyword
        self.date_since = date_since
        self.date_until = date_until
        self.fetcher = fetcher.Fetcher(date_since=date_since, date_until=date_until, keyword=keyword)


@click.group()
@click.option("-k", "--keyword", type=str, help="Issues with this keyword")
@click.option("-ds", "--date-since", type=click.DateTime(formats=["%Y-%m-%d"]), help="Issues since date in format "
                                                                                     "'YYYY-MM-DD'")
@click.option("-du", "--date-until", type=click.DateTime(formats=["%Y-%m-%d"]), help="Issues until date in format "
                                                                                     "'YYYY-MM-DD'")
@click.pass_context
def cli(ctx, keyword, date_since, date_until):
    """Fetch issues"""
    if date_since is not None:
        date_since = date_since.strftime("%Y-%m-%d")
    if date_until is not None:
        date_until = date_until.strftime("%Y-%m-%d")
    ctx.obj = Context(keyword, date_since, date_until)


@cli.command()
@click.pass_context
def containing_keyword(ctx):
    result = ctx.obj.fetcher.containing_keyword()
    print(result)


@cli.command()
@click.pass_context
def between_dates(ctx):
    result = ctx.obj.fetcher.between_dates()
    print(result)
