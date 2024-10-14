from typing import Optional

from app.core.constant.openai.interface import PriceInterface

class ChatPrice(PriceInterface):
    def __init__(
        self,
        model_name: str,
        input: float,
        output: float,
        cached_input: Optional[float] = None,
        reasoning_output: Optional[float] = None
    ):
        super().__init__(model_name)
        self.input = input                          # $/1M token
        self.output = output                        # $/1M token
        self.cached_input = cached_input            # $/1M token
        self.reasoning_output = reasoning_output    # $/1M token
    
    def calculate_usage_price(
        self,
        input_token: int,
        output_token: int,
        cached_input_token: int=None,
        reasoning_output_token: int=None
    ) -> float:
        price = (self.input * input_token + self.output * output_token)
        if cached_input_token:
            price += self.cached_input * cached_input_token
        if reasoning_output_token:
            price += self.reasoning_output * reasoning_output_token
        return price / 1_000_000
    
    def calculate_train_price(self) -> float:
        return None