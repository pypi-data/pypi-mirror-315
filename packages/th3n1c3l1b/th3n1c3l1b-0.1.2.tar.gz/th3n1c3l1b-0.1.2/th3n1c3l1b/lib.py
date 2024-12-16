"""Library for th3n1c3l1b
"""
from typing import Any, List, Mapping
import warnings
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
warnings.filterwarnings('ignore')

TIMEFORMAT_TIME = '%Y%m%d%H%M%S'


def members(obj: Any) -> Mapping[str, List[str]]:
    """Get Members of an Object

    Args:
        obj (Any): Object

    Returns:
        Mapping[str, List[str]]: Public Members of the Object
    """

    return {
        'vars': [
            attr for attr in dir(obj)
            if not callable(getattr(obj, attr)) and not attr.startswith("_")
        ],
        'methods': [
            attr for attr in dir(obj)
            if callable(getattr(obj, attr)) and not attr.startswith("_")
        ]
    }


def get_db(url: str) -> Engine:
    """Get database Engine
    Args:
        url (str): Database URL
    Returns:
        Engine: Database Engine
    """
    return create_engine(url)


def brokerage(
        buying_price: float,
        selling_price: float,
        quantity: int,
        broker_fees: float = 0,
        prescision: int = 2):
    """Brokerage Calculation
    Args:
        buying_price (float): Buying Price
        selling_price (float): Selling Price
        quantity (int): Quantity
        broker_fees (float, optional): Broker Fees. Defaults to 0.
        prescision (int, optional): Prescision. Defaults to 2.
    Returns:
        dict: Brokerage Calculation
    """
    turnover = (buying_price+selling_price)*quantity
    stt_total = selling_price * quantity * 0.001
    etc = 0.00053*turnover
    service_tax = .18*(broker_fees+etc)
    sebi_charges = turnover*0.000001
    stamp_charges = buying_price*quantity*0.00003
    total_tax = np.sum(
        [
            broker_fees,
            stt_total,
            etc,
            service_tax,
            sebi_charges,
            stamp_charges
        ]
    )
    breakeven = total_tax / quantity
    net_profit = ((selling_price - buying_price) * quantity) - total_tax
    return {
        'turnover': np.round(turnover, prescision),
        'stt_total': np.round(stt_total, prescision),
        'etc': np.round(etc, prescision),
        'sebi_charges': np.round(sebi_charges, prescision),
        'stamp_charges': np.round(stamp_charges, prescision),
        'breakeven': np.round(breakeven, prescision),
        'total_tax': np.round(total_tax, prescision),
        'net_profit': np.round(net_profit, prescision),
    }


def now() -> datetime:
    """Get Current Time
    Returns:
        datetime: Current Time
    """
    return datetime.now() + timedelta(hours=5, minutes=30)


def seconds_between(
        start: datetime,
        end: datetime
) -> int:
    """Seconds between start and end
    Args:
        start (datetime): Start Time
        end (datetime): End Time

    Returns:
        int: Seconds between start and end
    """
    return (end - start).days * 24 * 60 * 60 + (end - start).seconds
