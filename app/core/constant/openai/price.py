from app.core.constant.openai.interface import PriceInterface
from app.core.constant.openai.audio import AudioPrice
from app.core.constant.openai.chat import ChatPrice
from app.core.constant.openai.fine_tuning import FineTuningPrice
from app.core.constant.openai.image import ImagePrice
from app.core.constant.openai.embedding import EmbeddingPrice

class ModelPriceInterface:
    def find_model(self, model_name: str) -> PriceInterface:
        for model in self.__dict__.values():
            if model.model_name == model_name:
                return model
        
        return None
    
class ChatModelsPrice(ModelPriceInterface):
    GPT_35_TURBO = ChatPrice(model_name="gpt-3.5-turbo", input=0.5, output=1.5)
    GPT_35_TURBO_0125 = ChatPrice(model_name="gpt-3.5-turbo-0125", input=0.5, output=1.5)
    GPT_35_TURBO_1106 = ChatPrice(model_name="gpt-3.5-turbo-1106", input=1.0, output=2.0)
    GPT_35_TURBO_0613 = ChatPrice(model_name="gpt-3.5-turbo-0613", input=1.5, output=2.0)
    GPT_35_TURBO_0301 = ChatPrice(model_name="gpt-3.5-turbo-0301", input=1.5, output=2.0)
    GPT_35_TURBO_16K_0613 = ChatPrice(model_name="gpt-3.5-turbo-16k_0613",input=3.0, output=4.0)
    GPT_35_TURBO_INSTRUCT = ChatPrice(model_name="gpt-3.5-turbo-instruct", input=1.5, output=2.0)
    GPT_4 = ChatPrice(model_name="gpt-4", input=30.0, output=60.0)
    GPT_4_32k = ChatPrice(model_name="gpt-4-32k", input=60.0, output=120.0)
    GPT_4_TURBO = ChatPrice(model_name="gpt-4-turbo", input=10.0, output=30.0)
    GPT_4_TURBO_2024_04_09 = ChatPrice(model_name="gpt-4-turbo-2024-04-09", input=10.0, output=30.0)
    GPT_4_TURBO_PREVIEW = ChatPrice(model_name="gpt-4-turbo-preview", input=10.0, output=30.0)
    GPT_4_1106_preview = ChatPrice(model_name="gpt-4-1106-preview", input=10.0, output=30.0)
    O1_MINI = ChatPrice(model_name="o1-mini", input=3.0, cached_input=1.5, output=12.0)
    O1_MINI_2024_09_12 = ChatPrice(model_name="o1-mini-2024-09-12", input=3.0, cached_input=1.5, output=12.0)
    O1_PREVIEW = ChatPrice(model_name="o1-preview", input=15.0, cached_input=7.5, output=60.0)
    O1_PREVIEW_2024_09_12 = ChatPrice(model_name="o1-preview-2024-09-12", input=15.0, cached_input=7.5, output=60.0)
    GPT_4o_REALTIME_PREVIEW = ChatPrice(model_name="gpt-4o-realtime-preview", input=5.0, output=20.0)
    GPT_4o_REALTIME_PREVIEW_2024_10_01 = ChatPrice(model_name="gpt-4o-realtime-preview-2024-10-01", input=5.0, output=20.0)
    CHATGPT_4o_LATEST = ChatPrice(model_name="chatgpt-4o-latest", input=5.0, output=15.0)
    GPT_4o_MINI = ChatPrice(model_name="gpt-4o-mini", input=0.15, output=0.6, cached_input=0.075)
    GPT_4o_MINI_2024_07_18 = ChatPrice(model_name="gpt-4o-mini-2024-07-18", input=0.15, output=0.6, cached_input=0.075)
    GPT_4o = ChatPrice(model_name="gpt-4o", input=2.5, output=10.0, cached_input=1.25)
    GPT_4o_2024_08_26 = ChatPrice(model_name="gpt-4o-2024-08-26", input=2.5, output=10.0, cached_input=1.25)
    GPT_4o_2024_05_13 = ChatPrice(model_name="gpt-4o-2024-05-13", input=5.0, output=15.0)
    
class FineTunedChatModelsPrice(ModelPriceInterface):
    GPT_35_TURBO_0125 = FineTuningPrice(model_name="gpt-3.5-turbo-0125", input=3.0, output=6.0, train=8.0)
    GPT_4o_MINI_2024_07_18 = FineTuningPrice(model_name="gpt-4o-mini-2024-07-18", input=0.3, output=1.2, train=3.0)
    GPT_4o_2024_08_06 = FineTuningPrice(model_name="gpt-4o-2024-08-06", input=3.75, output=15.0, train=25.0)

class ImageModelsPrice(ModelPriceInterface):
    DALLE_2 = "dall-e-2"
    DALLE_3 = "dall-e-3"
    
class AudioModelsPrice(ModelPriceInterface):
    TTS_1 = AudioPrice(model_name="tts-1", input=15.0)
    TTS_1_HD = AudioPrice(model_name="tts-1-hd", input=30.0)
    GPT_4o_REALTIME_PREVIEW = AudioPrice(model_name="gpt-4o-realtime-preview", input=100.0, output=200.0)
    GPT_4o_REALTIME_PREVIEW_2024_10_01 = AudioPrice(model_name="gpt-4o-realtime-preview-2024-10-01", input=100.0, output=200.0)

class EmbeddingModelsPrice(ModelPriceInterface):
    TEXT_EMBEDDING_3_LARGE = EmbeddingPrice(model_name="text-embedding-3-large", input=0.13)
    TEXT_EMBEDDING_3_SMALL = EmbeddingPrice(model_name="text-embedding-3-small", input=0.02)
    TEXT_EMBEDDING_ADA_002 = EmbeddingPrice(model_name="text-embedding-ada-002", input=0.1)
    
class ModerationModelsPrice(ModelPriceInterface):
    OMNI_MODERATION_LATEST = "omni-moderation-latest"
    TEXT_MODERATION_LATEST = "text-moderation-latest"
    TEXT_MODERATION_STABLE = "text-moderation-stable"
    
    

class ModelsPrice:
    chat: ChatModelsPrice = ChatModelsPrice()
    fine_tuned_chat: FineTunedChatModelsPrice = FineTunedChatModelsPrice()
    embedding: EmbeddingModelsPrice = EmbeddingModelsPrice()
    audio: AudioModelsPrice = AudioModelsPrice()
    image: ImageModelsPrice = ImageModelsPrice()
    moderation: ModerationModelsPrice = ModerationModelsPrice()