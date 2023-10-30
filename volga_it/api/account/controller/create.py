from ..models import Account
from ..schemas import AccountCreate, AdminAccountCreate
from .authenticate import pwd_context


def create(data: AccountCreate | AdminAccountCreate):
    data.password = pwd_context.hash(data.password)
    return Account.create(**data.to_model_data())
