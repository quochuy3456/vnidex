import requests
from bs4 import BeautifulSoup
import numpy as np
import logging


class CrawlerFoodandDrink:
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

    def get_total_assets(self):
        """
        Tổng tài sản
        """
        try:
            tr = self.asset_data.find_all('tr', {'id': 'rptNhomChiTieu_ctl01_rptData_ctl01_TrData'})[0]
            dt = list(map(lambda x: float(x.get_text(strip=True).replace(",", "")) if x.get_text(strip=True) else 0, tr.find_all('td')[1:]))
            return np.array(dt)
        except IndexError:
            return np.array([0]*4)


    def get_capital(self):
        """
        Vốn chủ sở hữu
        """
        try:
            tr = self.asset_data.find_all('tr', {'id': 'rptNhomChiTieu_ctl01_rptData_ctl04_TrData'})[0]
            dt = list(map(lambda x: float(x.get_text(strip=True).replace(",", "")) if x.get_text(strip=True) else 0, tr.find_all('td')[1:]))
            self.capital = np.array(dt)[-1]
            return self.capital
        except IndexError:
            self.capital = 0
            return self.capital

    def get_total_revenue(self):
        """
        Tổng lợi nhận sau thuế
        """
        try:
            tr = self.asset_data.find_all('tr', {'id': 'rptNhomChiTieu_ctl00_rptData_ctl06_TrData'})[0]
            dt = list(map(lambda x: float(x.get_text(strip=True).replace(",", "")) if x.get_text(strip=True) else 0,
                          tr.find_all('td')[1:]))
            return np.array(dt)
        except IndexError:
            return np.array([0] * 4)

    def get_toc_do_tang_truong(self):
        get_total_assets = self.get_total_assets()
        zero_position = np.where(get_total_assets == 0)
        get_total_assets[zero_position] = 1
        g = self.get_total_revenue()/get_total_assets
        self.g = round(np.mean(g)*100, 2)
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

    def select_eps_value(self):
        try:
            self.eps =  min(self.get_eps("EPS cơ bản"), self.get_eps("EPS pha loãng"))
            if self.eps == None:
                return 0
            return self.eps
        except:
            self.eps = 0
            return self.eps

    def get_current_price(self):
        try:
            pr = self.index_data.find_all('div', {'class': 'dltlu-point eq'})[0]
            return float(pr.get_text(strip=True))
        except:
            pass

        try:
            pr = self.index_data.find_all('div', {'class': 'dltlu-point down'})[0]
            return float(pr.get_text(strip=True))
        except:
            pass

        try:
            pr = self.index_data.find_all('div', {'class': 'dltlu-point up'})[0]
            return float(pr.get_text(strip=True))
        except:
            pass

        try:
            pr = self.index_data.find_all('div', {'class': 'pri'})[0]
            return float(pr.get_text(strip=True))
        except:
            pass

        return 0.0


    def get_real_value_1(self):
        return round(self.select_eps_value()*(8.5 + 2 * self.get_toc_do_tang_truong()), 1)

    def get_real_value_2(self, lai_suat):
        return round((self.select_eps_value()*(8.5 + 2 * self.get_toc_do_tang_truong())*4.4)/float(lai_suat), 1)

    def get_real_value_3(self):
        capital = self.get_capital()
        KLDLH = self.get_eps("đang lưu hành")
        self.KLDLH = KLDLH
        BVPS = capital/KLDLH
        return round(np.sqrt(22.5*BVPS*self.select_eps_value()), 2)
