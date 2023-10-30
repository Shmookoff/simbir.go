from volga_it.api.account import Account

from ..models import Rent


def user_history(account: Account):
    return Rent.get_query().filter(Rent.user == account).order_by(Rent.time_start).all()
