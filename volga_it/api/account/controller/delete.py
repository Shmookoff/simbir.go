from ..models import Account


def delete(account: Account):
    return account.delete()
