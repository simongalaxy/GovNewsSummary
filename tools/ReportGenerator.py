from langchain_ollama import OllamaLLM
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document

import os
from dotenv import load_dotenv
load_dotenv()

class ReportGenerator:
    def __init__(self, logger):
        self.logger = logger 
        self.modelName = os.getenv("OLLAMA_LLM_MODEL")
        self.llm = OllamaLLM(
            model=self.modelName,
            temperature=0
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def generate_report(self, summarized_texts: list[str]):
        texts = []
        for text in summarized_texts:
            splitted_summarized_text = self.text_splitter.split_text(text)
            for item in splitted_summarized_text:
                texts.append(item)
            
        docs = [Document(page_content=t) for t in texts]
        chain = load_summarize_chain(
            llm=self.llm, 
            chain_type='refine'
            )
        report = chain.run(docs)
        
        self.logger.info("Daily Press Release Report:\n")
        self.logger.info(report)
        self.logger.info("*"*100)
        
        return report
    