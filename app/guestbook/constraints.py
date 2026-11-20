from django.db.models import F, Q


def implies(condition, consequence):
    return ~condition | consequence


def iff(left, right):
    return (left & right) | (~left & ~right)


def not_earlier_than(field, reference):
    return Q(**{f"{field}__isnull": True}) | Q(**{f"{field}__gte": F(reference)})
