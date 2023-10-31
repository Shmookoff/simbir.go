from volga_it.api.account.schemas import AccountUpdate, AdminAccountUpdate

from ..models import Account
from .authenticate import process_new_data


def update(account: Account, data: AccountUpdate | AdminAccountUpdate):
    data = process_new_data(data)
    return account.update(**data.to_model_data())
