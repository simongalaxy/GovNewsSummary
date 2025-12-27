import os
from pathlib import Path

def write_report(url:str, text: str) -> str:
    #daily_url = "https://www.info.gov.hk/gia/general/202512/03.htm"
    
    # generate filename by daily press release url.
    splitted_url = url.split("/")
    yearMonth = splitted_url[-2]
    day = splitted_url[-1].split(".")[0]
    
    filename = f"Daily_PressRelease_Report_{yearMonth}{day}.txt"
    filepath = "./reports/"
    
    # generate report in text file.
    with open(os.path.join(filepath, filename), "w") as f:
        f.write(text)
        
    return filename
        