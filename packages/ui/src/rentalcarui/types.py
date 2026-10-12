from __future__ import annotations
from typing import Literal


type LicensePlate = str
type CustomerID = int

CUSTOMER_ID_UNSET: CustomerID = 0

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
