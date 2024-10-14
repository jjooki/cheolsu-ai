import abc
import requests

from datetime import datetime, timedelta
from typing import Optional

class PriceInterface(metaclass=abc.ABCMeta):
    def __init__(self, model_name: str):
        self.model_name: str = model_name
        self.exchange_rate: Optional[float] = None
        self.exchange_update_date: Optional[datetime] = None
        
    @abc.abstractmethod
    def calculate_usage_price(self, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    def calculate_train_price(self, **kwargs):
        raise NotImplementedError
    
    def _convert_unit(self, unit: str = "o") -> dict:
        result = {}
        
        unit = unit.lower()
        convertor = 0
        match unit:
            case "o":
                convertor = 1 / 1_000_000
            case "k":
                convertor = 1 / 1_000
            case "m":
                convertor = 1
            case "g":
                convertor = 1_000
            case "t":
                convertor = 1_000_000
            case _:
                raise ValueError("Invalid unit")
            
        for key, value in self.__dict__.items():
            if isinstance(value, (int, float)):
                result.update({key: value * convertor})
        
        return result
    
    def _set_exchange_rate(self, currency: str = "KRW") -> None:
        currency = currency.lower()
        url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
        try:
            res = requests.get(url).json()
            
        except Exception as e:
            raise ValueError(f"Failed to get exchange rate: {e}")
        
        self.exchange_rate = res['usd'][currency]
        self.exchange_update_date = datetime.now()
        
    def convert_currency(self, cost: float, currency: str = "KRW") -> dict:
        if self.exchange_rate and self.exchange_update_date:
            if datetime.now() - self.exchange_update_date < timedelta(hours=8):
                return self.exchange_rate * cost
        
        self._set_exchange_rate(currency)
        return self.exchange_rate * cost
        