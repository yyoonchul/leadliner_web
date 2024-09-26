import requests
import pandas as pd
from bs4 import BeautifulSoup
import io
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
openai_api_key = os.getenv("OPENAI_API_KEY")

class MakeUserNews:
    def __init__(self, client_id=client_id, client_secret=client_secret, openai_api_key=openai_api_key):
        self.client_id = client_id
        self.client_secret = client_secret
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

        
    def get_naver_news(self, keyword, lines: int=30):
        
        #네이버 뉴스에서 키워드를 검색하고 요약 정보를 추출하여 CSV 형식을 문자열로 반환
        
        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }
        params = {
            "query": keyword,
            "sort": "sim",
            "start": 1,
            "display": lines,
        }

        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response.status_code == 200 and response_data["items"]:
            news_list = response_data["items"]
        else:
            return f"Error: {response.status_code}, {response_data.get('errorMessage')}"

        df = pd.DataFrame(news_list)[["title", "description"]]
        df.columns = ["제목", "본문"]

        # HTML 태그 제거 및 본문 링크 추가
        df["제목"] = df["제목"].astype(str).apply(lambda x: BeautifulSoup(x, "lxml").text)
        df["본문"] = df["본문"].astype(str).apply(lambda x: BeautifulSoup(x, "lxml").text)

        result = "\n".join(df["제목"] + "\n" + df["본문"])

        return result
    
    def summarize_news(self, text:str):
        # OpenAI ChatGPT API를 사용하여 텍스트 요약
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a news summarizer specialized in stock news briefings."},
                {"role": "user", "content": f"오늘의 뉴스 헤드라인을 모아놓은 다음 텍스트를 읽고 3개의 주요 뉴스를 요약해줘. 각각의 요약은 한 문장으로 적어줘. 주제가 바뀌면 줄바꿈으로 구분해서 총 두번의 줄바꿈으로 구분해줘. 번호 없이 문장만을 적어줘.:\n\n{text}"},
                ]
        )

        summary = response.choices[0].message.content
        summary_list = summary.strip().split('\n')
        if len(summary_list) >3:
            for item in summary_list:
                if item == "":
                    summary_list.remove(item)
        return summary_list

    def make_user_news(self, keyword:str):
        news = self.get_naver_news(keyword, 30)
        summary = self.summarize_news(news)
        if len(summary) == 3:
            return summary
        elif len(summary) > 3:
            for item in summary:
                if item == "":
                    summary.remove(item)
            return summary[:3]
        else:
            while len(summary) < 3:
                summary.append("")
            return summary
    