from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

class SummaryConsolidator:
    def __init__(self, logger):
        self.logger = logger
        self.modelName = os.getenv("OLLAMA_LLM_MODEL")
        self.llm = ChatOllama(
            model=self.modelName,
            temperature=0.2
        )
        self.promp_template = """
            You are a report generator.

            You will receive a list of summaries.
            Your task is to merge them into a single, coherent, comprehensive, categorized and multi-paragraph Markdown report.

            ### Requirements
            - Produce a clean, structured Markdown document.
            - Remove redundancy.
            - Improve clarity and flow.
            - Add a short introduction and conclusion.
            - Keep the tone neutral and factual.
            - Group all the summaries by its nature.
            - Do NOT compress. Write in multiple paragraphs.

            ### Input summaries:
            {summaries}

            ### Now produce the consolidated Markdown report:
            """
        self.prompt = ChatPromptTemplate.from_template(self.promp_template)
    
    
    def consolidate_summary(self, summaries) -> str:
        
        summaries_text = "\n".join(f"- {s}" for s in summaries)
        
        chain = self.prompt | self.llm
        response = chain.invoke({"summaries": summaries_text})
        
        return response.content
        