from app.core.constant.openai.interface import PriceInterface

class ImagePrice(PriceInterface):
    def __init__(self, model_name: str, output: float):
        super().__init__(model_name)
        self.output: float = output    # $/1M token
    
    def calculate_usage_price(self, num: int) -> float:
        return self.output * num
    
    def calculate_train_price(self) -> float:
        return None
