from typing import Optional

from app.core.constant.openai.interface import PriceInterface

class FineTuningPrice(PriceInterface):
    def __init__(
        self,
        model_name: str,
        input: float,
        output: float,
        train: float,
        cached_input: Optional[float] = None
    ):
        super().__init__(model_name)
        self.input: float = input               # $/1M token
        self.output: float = output             # $/1M token
        self.train: float = train               # $/1M token
        self.cached_input: float = cached_input # $/1M token
        
    def calculate_usage_price(
        self,
        input_token: int,
        output_token: int,
        cached_input_token: int=None,
    ) -> float:
        price = (self.input * input_token + self.output * output_token)
        if cached_input_token:
            price += self.cached_input * cached_input_token
        return price / 1_000_000
    
    def calculate_train_price(self, train_token: int) -> float:
        return self.train * train_token / 1_000_000
        