from typing import Optional

from app.core.constant.openai.interface import PriceInterface

class AudioPrice(PriceInterface):
    def __init__(
        self,
        model_name: str,
        input: float,
        output: Optional[float] = 0.0
    ):
        super().__init__(model_name)
        self.input = input              # $/1M token
        self.output = output            # $/1M token
    
    def calculate_usage_price(self, input_token: int, output_token: int) -> float:
        return (self.input * input_token + self.output * output_token) / 1_000_000
    
    def calculate_train_price(self) -> float:
        return None
    
    def calculate_cached_usage_price(self):
        return None
    

class AudioTextPrice(PriceInterface):
    def __init__(
        self,
        model_name: str,
        input: float,
        output: Optional[float] = None
    ):
        super().__init__(model_name)
        self.input = input              # $/1M token
        self.output = output            # $/1M token
    
    def calculate_usage_price(self, input_token: int, output_token: int) -> float:
        return (self.input * input_token + self.output * output_token) / 1_000_000
    
    def calculate_train_price(self) -> float:
        return None
    
    def calculate_cached_usage_price(self):
        return None