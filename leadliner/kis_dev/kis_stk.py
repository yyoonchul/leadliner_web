import leadliner.kis_dev.kis_auth as kis
import pandas as pd
# import time, copy
# import requests
# import json
# from collections import namedtuple
# from datetime import datetime
# from pandas import DataFrame

# 주식현재가 시세 Object를 DataFrame 으로 반환
# Input: None (Option) 상세 Input값 변경이 필요한 경우 API문서 참조
# Output: DataFrame (Option) output
def get_inquire_price(div_code="J", itm_no="", tr_cont="", FK100="", NK100="", dataframe=None):  # [국내주식] 기본시세 > 주식현재가 시세
    url = '/uapi/domestic-stock/v1/quotations/inquire-price'
    tr_id = "FHKST01010100" # 주식현재가 시세

    params = {
        "FID_COND_MRKT_DIV_CODE": div_code, # 시장 분류 코드  J : 주식/ETF/ETN, W: ELW
        "FID_INPUT_ISCD": itm_no            #   종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    }
    res = kis._url_fetch(url, tr_id, tr_cont, params)

    # Assuming 'output' is a dictionary that you want to convert to a DataFrame
    current_data = pd.DataFrame(res.getBody().output, index=[0])  # getBody() kis_auth.py 존재

    dataframe = current_data

    return dataframe

def get_overseas_price_quot_price(excd="", itm_no="", tr_cont="", dataframe=None):
    url = '/uapi/overseas-price/v1/quotations/price'
    tr_id = "HHDFS00000300" # 해외주식 현재체결가

    params = {
        "AUTH": "",             # 사용자권한정보 : 사용안함
        "EXCD": excd,           # 거래소코드 	HKS : 홍콩,NYS : 뉴욕,NAS : 나스닥,AMS : 아멕스,TSE : 도쿄,SHS : 상해,SZS : 심천,SHI : 상해지수
                                #           SZI : 심천지수,HSX : 호치민,HNX : 하노이,BAY : 뉴욕(주간),BAQ : 나스닥(주간),BAA : 아멕스(주간)
        "SYMB": itm_no          # 종목번호
    }
    res = kis._url_fetch(url, tr_id, tr_cont, params)

    # Assuming 'output' is a dictionary that you want to convert to a DataFrame
    current_data = pd.DataFrame(res.getBody().output, index=[0])

    dataframe = current_data

    return dataframe


#미국 주식 주간 시세 이슈 해결 시 사용할 수 있는 함수
# def get_overseas_price_quot_dailyprice(excd="", itm_no="", gubn="", bymd="", modp="0", tr_cont="", dataframe=None):
#     url = '/uapi/overseas-price/v1/quotations/dailyprice'
#     tr_id = "HHDFS76240000" # 해외주식 기간별시세

#     if bymd is None:
#         bymd = datetime.today().strftime("%Y%m%d")   # 종료일자 값이 없으면 현재일자

#     params = {
#         "AUTH": "",             # (사용안함) 사용자권한정보
#         "EXCD": excd,           # 거래소코드 	HKS : 홍콩,NYS : 뉴욕,NAS : 나스닥,AMS : 아멕스,TSE : 도쿄,SHS : 상해,SZS : 심천,SHI : 상해지수
#                                 #           SZI : 심천지수,HSX : 호치민,HNX : 하노이,BAY : 뉴욕(주간),BAQ : 나스닥(주간),BAA : 아멕스(주간)
#         "SYMB": itm_no,         # 종목번호
#         "GUBN": gubn,           # 일/주/월구분 0:일. 1:주, 2:월
#         "BYMD": bymd,           # 조회기준일자(YYYYMMDD) ※ 공란 설정 시, 기준일 오늘 날짜로 설정
#         "MODP": modp,           # 수정주가반영여부 0 : 미반영, 1 : 반영
#         "KEYB": ""              # (사용안함) NEXT KEY BUFF  응답시 다음값이 있으면 값이 셋팅되어 있으므로 다음 조회시 응답값 그대로 셋팅
#     }
#     res = kis._url_fetch(url, tr_id, tr_cont, params)

#     # Assuming 'output' is a dictionary that you want to convert to a DataFrame
#     current_data = pd.DataFrame(res.getBody().output2)

#     dataframe = current_data

#     return dataframe