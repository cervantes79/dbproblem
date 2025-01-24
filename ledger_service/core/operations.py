from enum import Enum
from typing import Set


class BaseLedgerOperations(str, Enum):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    @classmethod
    def values(cls) -> Set[str]:
        return {item.value for item in cls}


OPERATION_VALUES = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
}
