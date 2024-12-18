from .getWithdraw import GetWithdraw
from .reqWithdraw import RequestWithdraw

class Withdraw(GetWithdraw, RequestWithdraw):
    pass
