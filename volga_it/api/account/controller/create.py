from ..models import Account
from ..schemas import AccountCreate, AdminAccountCreate
from .authenticate import process_new_data


def create(data: AccountCreate | AdminAccountCreate):
    data = process_new_data(data)
    return Account.create(**data.to_model_data())
