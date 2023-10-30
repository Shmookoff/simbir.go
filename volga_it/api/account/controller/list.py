from ..models import Account


def list(limit: int, offset: int):
    return Account.get_query().limit(limit).offset(offset).all()
