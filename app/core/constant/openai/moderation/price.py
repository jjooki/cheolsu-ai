from app.core.constant.openai.interface import PriceInterface

class ModerationPrice(PriceInterface):
    def __init__(self, model_name: str, input: float):
        super().__init__(model_name)    # model name. ex) gpt-3.5-turbo
        self.input: float = input       # $/1M token
    
    def calculate_usage_price(self, input_token: int) -> float:
        return (self.input * input_token) / 1_000_000
    
    def calculate_train_price(self) -> float:
        return None