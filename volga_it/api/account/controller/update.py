from volga_it.api.account.schemas import AccountUpdate, AdminAccountUpdate

from ..models import Account


def update(account: Account, data: AccountUpdate | AdminAccountUpdate):
    return account.update(**data.to_model_data())
