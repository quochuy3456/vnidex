import requests
from bs4 import BeautifulSoup
import numpy as np
import logging


class Crawler:
    def __init__(self, cpn_code):
        self.path_get_asset_info = f'https://s.cafef.vn/Ajax/Bank/BHoSoCongTy.aspx?symbol={cpn_code}&Type=2&PageIndex=0&PageSize=4&donvi=1'
        self.path_get_index_info = f"https://s.cafef.vn/hose/{cpn_code.upper()}-.chn"
        self.asset_data = None
        self.index_data = None
        self.capital = None
        self.KLDLH = None
        self.g = None
        self.eps = None
        self._data()


    def _data(self):
        self.asset_data = BeautifulSoup(requests.get(self.path_get_asset_info).text, "html.parser")
        self.index_data = BeautifulSoup(requests.get(self.path_get_index_info).text, "html.parser")

    def get_item_data(self, item):
        logging.info(f'Parser {item}')
        for tr in self.asset_data.find_all('tr'):
            if item in tr.get_text():
                dt = list(map(lambda x: float(x.get_text(strip=True).replace(",", "")) if x.get_text(strip=True) else 0, tr.find_all('td')[1:]))
                return np.array(dt)
        return None

    def get_toc_do_tang_truong(self):
        self.g = round(np.mean(self.get_item_data("Tổng doanh thu")/self.get_item_data("Tổng tài sản"))*100, 2)
        return self.g

    def get_eps(self, text):
        logging.info(f'Parser {text}')
        try:
            d = self.index_data.find(text=text).find_parents('li')[0]
        except:
            for i in self.index_data.find_all("li"):
                if text in i.get_text(strip=True):
                    d = i
                    break
        try:
            return float(d.find_all('span')[1].get_text(strip=True).replace(",", ""))
        except:
            return float(d.find_all('div')[1].get_text(strip=True).replace(",", ""))
        return 0

    def select_eps_value(self):
        try:
            self.eps =  min(self.get_eps("EPS cơ bản"), self.get_eps("EPS pha loãng"))
            return self.eps
        except:
            print("Error EPS")
            return 0.000001

    def get_real_value_1(self):
        return round(self.select_eps_value()*(8.5 + 2 * self.get_toc_do_tang_truong()), 1)

    def get_real_value_2(self, lai_suat):
        return round((self.select_eps_value()*(8.5 + 2 * self.get_toc_do_tang_truong())*4.4)/float(lai_suat), 1)

    def get_real_value_3(self):
        capital = self.get_item_data("Vốn và các quỹ")[-1]
        KLDLH = self.get_eps("đang lưu hành")
        self.capital = capital
        self.KLDLH = KLDLH
        BVPS = capital/KLDLH
        return round(np.sqrt(22.5*BVPS*self.select_eps_value()), 2)
