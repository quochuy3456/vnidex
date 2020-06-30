from django.shortcuts import render
from vnidxCrawl.views.banks import Crawler

# Create your views here.
def bank(request):
    cpn_code = request.GET.get('cpn_code')
    lai_suat_input = request.GET.get('lai_suat')
    if not cpn_code:
        return render(request, 'vnidxUI/index.html')

    lst_input = cpn_code.split(",")
    lst_lai_suat = ["0"]*len(lst_input)
    if len(lai_suat_input.split(",")) <= len(lst_input):
        lst_lai_suat[0:len(lai_suat_input.split(","))-1] = lai_suat_input.split(",")
    else:
        lst_lai_suat = lai_suat_input.split(",")[0:len(lst_input)]

    lst_re = [['Cpn Code', 'Chỉ số EPS', 'Tổng tài sản', 'KLDLH', 'Tốc độ tăng trưởng', 'Gía hiện tại', 'Lãi suất', 'Giá trị thực 1', 'Gía trị thực 2', 'Gía trị thực 3', 'Kết luận']]
    for bk in range(len(lst_input)):
        crawler = Crawler(lst_input[bk].strip())
        value1 = crawler.get_real_value_1()
        value2 = crawler.get_real_value_2(float(lst_lai_suat[bk].strip())) if lai_suat_input else "Nhập lãi suất gửi/năm để tính"
        value3 = crawler.get_real_value_3()
        EPS = crawler.eps
        capital = crawler.capital
        KLDLH = crawler.KLDLH
        rising_speed = crawler.g
        current_price = crawler.get_current_price()
        print(current_price)
        lai_suat = float(lst_lai_suat[bk].strip()) if lai_suat_input else "Nhập lãi suất gửi/năm để tính",
        result = "Có thể mua" if current_price < value3 else "Nên xem xét"
        summ = [lst_input[bk].upper(), EPS, capital, KLDLH, rising_speed, current_price, lai_suat, value1, value2, value3, result]
        lst_re.append(summ)
    return render(request, 'vnidxUI/index.html', {'data':lst_re, 'cpn_code': cpn_code, 'lai_suat': lai_suat_input})

def travel(request):
    pass