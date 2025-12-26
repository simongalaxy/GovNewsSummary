from langchain_ollama import OllamaLLM
from langchain_text_splitters import CharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.docstore.document import Document

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

class ContentSummarizer:
    def __init__(self): 
        self.model = os.getenv("OLLAMA_SUMMARIZATION_MODEL")
        self.llm = OllamaLLM(
            model=self.model,
            temperature=0.3
        )
        self.text_splitter = CharacterTextSplitter()

    
    async def summarize_content(self, content: str):
        texts = self.text_splitter.split_text(content)
        docs = [Document(page_content=t) for t in texts]
        chain = load_summarize_chain(llm=self.llm, chain_type='map_reduce')
        
        return chain.run(docs)
    
        
    async def summarize_all_news_content(self, documents):
        tasks = [self.summarize_content(content=document.page_content) for document in documents]
        results = await asyncio.gather(*tasks)
        
        print(f"Total news page scraped: {len(results)}")
        for result in results:
            print(result)
        
        return results
        