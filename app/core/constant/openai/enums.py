from enum import Enum

class ChatModelsEnum(Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_35_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_35_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_35_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_35_TURBO_16K_0613 = "gpt-3.5-turbo-16k_0613"
    GPT_35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_TURBO_2024_04_09 = "gpt-4-turbo-2024-04-09"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"
    GPT_4_1106_preview = "gpt-4-1106-preview"
    O1_MINI = "o1-mini"
    O1_MINI_2024_09_12 = "o1-mini-2024-09-12"
    O1_PREVIEW = "o1-preview"
    O1_PREVIEW_2024_09_12 = "o1-preview-2024-09-12"
    GPT_4o_REALTIME_PREVIEW = "gpt-4o-realtime-preview"
    GPT_4o_REALTIME_PREVIEW_2024_10_01 = "gpt-4o-realtime-preview-2024-10-01"
    GPT_4o_MINI = "gpt-4o-mini"
    GPT_4o_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
    GPT_4o = "gpt-4o"
    GPT_4o_2024_08_26 = "gpt-4o-2024-08-26"
    GPT_4o_2024_05_13 = "gpt-4o-2024-05-13"
    CHATGPT_4o_LATEST = "chatgpt-4o-latest"

class FineTunedChatModelsEnum(Enum):
    GPT_35_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT_4o_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
    GPT_4o_2024_08_06 = "gpt-4o-2024-08-06"

class ImageModelsEnum(Enum):
    DALLE_2 = "dall-e-2"
    DALLE_3 = "dall-e-3"
    
class AudioModelsEnum(Enum):
    TTS_1 = "tts-1"
    TTS_1_HD = "tts-1-hd"
    GPT_4o_REALTIME_PREVIEW = "gpt-4o-realtime-preview"
    GPT_4o_REALTIME_PREVIEW_2024_10_01 = "gpt-4o-realtime-preview-2024-10-01"

class EmbeddingModelsEnum(Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    
class ModerationModelsEnum(Enum):
    OMNI_MODERATION_LATEST = "omni-moderation-latest"
    TEXT_MODERATION_LATEST = "text-moderation-latest"
    TEXT_MODERATION_STABLE = "text-moderation-stable"


class ModelsEnum:
    chat: ChatModelsEnum = ChatModelsEnum()
    fine_tuned_chat: FineTunedChatModelsEnum = FineTunedChatModelsEnum()
    embedding: EmbeddingModelsEnum = EmbeddingModelsEnum()
    audio: AudioModelsEnum = AudioModelsEnum()
    image: ImageModelsEnum = ImageModelsEnum()
    moderation: ModerationModelsEnum = ModerationModelsEnum()