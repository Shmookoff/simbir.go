from ..models import Rent


def delete(rent: Rent):
    return rent.delete()
