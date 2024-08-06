import requests
import pandas as pd
from bs4 import BeautifulSoup
import io


class MakeUserNews:
    def __init__(self, client_id="qt27ngYl4fLAuIO8LIr8", client_secret="C7D2679Ddq"):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_naver_news(self, keyword):
        
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
            "display": 10,
        }

        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response.status_code == 200 and response_data["items"]:
            news_list = response_data["items"]
        else:
            return f"Error: {response.status_code}, {response_data.get('errorMessage')}"

        df = pd.DataFrame(news_list)[["title", "link", "description"]]
        df.columns = ["제목", "링크", "본문"]
        df["키워드"] = keyword

        # HTML 태그 제거 및 본문 링크 추가
        df["제목"] = df["제목"].astype(str).apply(lambda x: BeautifulSoup(x, "lxml").text)
        df["본문"] = df["본문"].astype(str).apply(lambda x: BeautifulSoup(x, "lxml").text)
        # CSV 데이터 생성 (문자열 형태)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
        csv_data = csv_buffer.getvalue()

        return csv_data

    def make_merged_news(self, keywords):
        
        #여러 키워드에 대한 뉴스 검색 결과를 하나의 CSV 형식 문자열로 반환

        all_data = []

        for keyword in keywords:
            csv_data = self.get_naver_news(keyword)
            if csv_data.startswith("Error"):
                return "Error"

            df = pd.read_csv(io.StringIO(csv_data))
            all_data.append(df)

        if all_data:
            merged_df = pd.concat(all_data, ignore_index=True)
            csv_buffer = io.StringIO()
            merged_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_data = csv_buffer.getvalue()
            return csv_data
        else:
            return "Error"