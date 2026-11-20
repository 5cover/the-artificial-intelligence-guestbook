def implies(condition, consequence):
    return ~condition | consequence


def iff(left, right):
    return (left & right) | (~left & ~right)
