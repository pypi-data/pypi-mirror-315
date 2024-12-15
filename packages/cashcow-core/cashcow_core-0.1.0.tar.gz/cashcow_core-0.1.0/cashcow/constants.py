"""Cashcow constants"""

from enum import StrEnum


class Currency(StrEnum):
    """Currency constants"""

    KRW = "KRW"
    USD = "USD"


class ConnectionType(StrEnum):
    """Connection type constants"""

    SHINHAN_BANK = "shinhan_bank"
    SHINHAN_CARD = "shinhan_card"
    SHINHAN_INVESTMENT = "shinhan_investment"


class BankType(StrEnum):
    """Bank type constants"""

    SHINHAN_BANK = "shinhan_bank"


class CardType(StrEnum):
    """Card type constants"""

    SHINHAN_CARD = "shinhan_card"


class InvestmentType(StrEnum):
    """Investment type constants"""

    SHINHAN_INVESTMENT = "shinhan_investment"


class AccountType(StrEnum):
    """Account type constants"""

    SHINHAN_BANK = "shinhan_bank"
    SHINHAN_INVESTMENT = "shinhan_investment"
