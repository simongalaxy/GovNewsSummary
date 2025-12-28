from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.docstore.document import Document
from langchain_core.prompts import PromptTemplate

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

class ContentSummarizer:
    def __init__(self, logger):
        self.logger = logger 
        self.modelName = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.llm = OllamaLLM(
            model=self.modelName,
            temperature=0
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        # self.detailed_prompt = PromptTemplate(
        #     input_variables=["text"],
        #     template="""
        #     Write a **detailed, multi-paragraph summary** of the following text.
        #     Include all important context, numbers, name and implications.
            
        #     Text:
        #     {text}
            
        #     Detailed Summary:
        #     """
        # )

    
    async def summarize_content(self, content: str):
        texts = self.text_splitter.split_text(content)
        self.logger.info(f"total no. of text splitted: {len(texts)}")
        docs = [Document(page_content=t) for t in texts]
        chain = load_summarize_chain(
            llm=self.llm, 
            chain_type='refine',
            # question_prompt=self.detailed_prompt,
            # refine_prompt=self.detailed_prompt,
            )
        summary = chain.run(docs)
        
        self.logger.info("Original Press Release:\n")
        self.logger.info(content)
        self.logger.info("-"*100)
        self.logger.info("Summary:\n")
        self.logger.info(summary)
        self.logger.info("*"*100)
        self.logger.info(f"Data type of summary: {type(summary)}")
        
        return summary
    
        
    async def summarize_all_news_content(self, documents):
        tasks = [self.summarize_content(content=document[0].page_content.strip()) for document in documents]
        summarized_texts = await asyncio.gather(*tasks)
        
        return summarized_texts
        