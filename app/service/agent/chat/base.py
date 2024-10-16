# import asyncio
# import logging

# from typing import List

# from langsmith import traceable
# import os

# from app.services.generator.generator import GeneratorServiceV2

# tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# # from app.routers.chat_v2.components.translator_llm import arun_english  # Import the translation function
# logging.basicConfig(level=logging.INFO)


# class ChatAgent(BaseAgent):
#     def __init__(
#         self,
#         stock_info_repository: StockInfoRepository,
#         stock_chart_repository: StockChartRepository,
#         ca_repository: CaRepository,
#         finance_repository: FinanceRepository,
#     ) -> None:
#         super().__init__(
#             stock_info_repository=stock_info_repository,
#             stock_chart_repository=stock_chart_repository,
#             ca_repository=ca_repository,
#             finance_repository=finance_repository,
#         )
#         self.generate_service = GeneratorService()
#         self.classification_agent = ClassificationAgent()
#         self.search_agent = StockNameSearch(stock_info_repository)
#         self.stock_infos = []
#         self.history_limit = 2

#         self.system_prompt = """
# Let's think step by step.
# You are an AI concierge specializing in wealth management.
# You are having a conversation with a Japanese customer.

# 1. Answer user's query in Japanese !
# 2. Your answers should not utilize any additional information beyond the given information.
# 3. If you don't know the answer, don't make up the answer, just say you don't know.
# 4. Do not use profanity.
# 5. Be super polite in your interaction and adhere to Japanese's customs.
# 6. Cite analyst comments when giving recommendations.
# 7. Respond in a structured markdown format, put emphasis and stock name in bold.

# Information:
# {information}
# """