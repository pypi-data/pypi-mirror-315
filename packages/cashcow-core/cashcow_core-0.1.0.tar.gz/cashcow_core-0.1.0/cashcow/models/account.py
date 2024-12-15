"""Bank model definition"""

from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Interval, Numeric, String

from cashcow.constants import AccountType, Currency
from cashcow.models.base import MetadataMixin, PipelineORMModel, TimestampMixin


class Account(PipelineORMModel, MetadataMixin):
    """Account model"""

    __tablename__: str = "accounts"

    connection_id: int = Column(Integer, ForeignKey("connections.id"), nullable=False)
    """ID of the connection"""

    identifier: str = Column(String, nullable=False)
    """Identifier of the account"""
    name: str = Column(String, nullable=False)
    """Name of the account"""
    type: AccountType = Column(String, nullable=False)
    """Type of the account"""
    currency: Currency = Column(String, nullable=False)
    """Currency of the account"""

    product_name: str = Column(String, nullable=False)
    """Name of the product"""
    product_description: str = Column(String)
    """Description of the product"""

    period: timedelta = Column(Interval)
    """Period of the product"""
    start_date: datetime = Column(DateTime)
    """Start date of the product"""
    end_date: datetime = Column(DateTime)
    """End date of the product"""

    def __repr__(self) -> str:
        return f"<Account {self.name} ({self.identifier})>"

    def __str__(self) -> str:
        return self.__repr__()


class Transaction(PipelineORMModel, TimestampMixin, MetadataMixin):
    """Transaction model"""

    __tablename__: str = "transactions"

    account_id: int = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    """ID of the account"""

    branch: str = Column(String)
    """Branch of the transaction"""
    category: str = Column(String, nullable=False)
    """Category of the transaction"""
    amount: Decimal = Column(Numeric(12, 4), nullable=False)
    """Amount of the transaction"""
    destination: str = Column(String)
    """Identifier of the destination"""
    currency: Currency = Column(String, nullable=False)
    """Currency of the transaction"""

    balance_amount: Decimal = Column(Numeric(12, 4), nullable=False)
    """Balance amount of the account after the transaction (follows the currency of account)"""

    transaction_time: datetime = Column(DateTime, nullable=False)
    """Transaction time"""
