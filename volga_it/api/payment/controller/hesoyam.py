from volga_it.api.account import Account


def hesoyam(account: Account):
    account.update(balance=account.balance + 250_000)
