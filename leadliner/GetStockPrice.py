import leadliner.kis_dev.kis_auth as ka
import leadliner.kis_dev.kis_stk as kb
import pandas as pd
import sys

class GetStockPrice:
    def __init__(self):
        #토큰 발급 kis_auth import
        ka.auth()

    def korea_stock_price(self, code):
        data = kb.get_inquire_price(itm_no=code)
        price = data.stck_prpr.values[0]
        rate = data.prdy_ctrt.values[0]
        return price, rate
    
    def usa_stock_price(self, code):
        data = kb.get_overseas_price_quot_price(excd="NAS", itm_no=code)
        price = data.base.values[0]
        if price:
            rate = data.rate.values[0]
            return price, rate
        else:
            data = kb.get_overseas_price_quot_price(excd="NYS", itm_no=code)
            price = data.base.values[0]
            if price:
                rate = data.rate.values[0]
                return price, rate
            else:
                data = kb.get_overseas_price_quot_price(excd="AMS", itm_no=code)
                price = data.base.values[0]
                rate = data.rate.values[0]
                return price, rate