from django.shortcuts import render
from vnidxBank.views.banks import CrawlerBank
from vnidxFoodAndDrink.views.foodanddrink import CrawlerFoodandDrink

# Create your views here.
def redirect_page(request):
    return render(request, 'vnidxBase/redirect_page.html')

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

    lst_re = [['Mã công ty', 'Chỉ số EPS', 'Tổng tài sản', 'KLDLH', 'Tốc độ tăng trưởng', 
                'Giá hiện tại', 'Lãi suất', 'Giá trị thực 1', 'Giá trị thực 2', 'Giá trị thực 3', 'Kết luận']]
    for bk in range(len(lst_input)):
        crawler = CrawlerBank(lst_input[bk].strip())
        value1 = crawler.get_real_value_1()
        value2 = crawler.get_real_value_2(float(lst_lai_suat[bk].strip())) if lai_suat_input else "Nhập lãi suất trái phiếu để tính"
        value3 = crawler.get_real_value_3()
        EPS = crawler.eps
        capital = crawler.capital
        KLDLH = crawler.KLDLH
        rising_speed = crawler.g
        current_price = crawler.get_current_price()
        lai_suat = float(lst_lai_suat[bk].strip()) if lai_suat_input else "Nhập lãi suất trái phiếu để tính",
        result = "Có thể mua" if current_price < value3 else "Nên xem xét"
        summ = [lst_input[bk].upper(), EPS, capital, KLDLH, rising_speed, current_price, lai_suat, value1, value2, value3, result]
        lst_re.append(summ)
    lst_re = list(zip(*lst_re))
    return render(request, 'vnidxUI/index.html', {'data':lst_re, 'cpn_code': cpn_code, 'lai_suat': lai_suat_input})

def footanddrink(request):
    cpn_code = request.GET.get('cpn_code')
    lai_suat_input = request.GET.get('lai_suat')
    if not cpn_code:
        return render(request, 'vnidxFootAndDrink/footanddrink.html')

    lst_input = cpn_code.split(",")
    lst_lai_suat = ["0"] * len(lst_input)
    if len(lai_suat_input.split(",")) <= len(lst_input):
        lst_lai_suat[0:len(lai_suat_input.split(",")) - 1] = lai_suat_input.split(",")
    else:
        lst_lai_suat = lai_suat_input.split(",")[0:len(lst_input)]

    lst_re = [['Mã công ty', 'Chỉ số EPS', 'Tổng tài sản', 'KLDLH', 'Tốc độ tăng trưởng', 'Giá hiện tại', 'Lãi suất',
               'Giá trị thực 1', 'Giá trị thực 2', 'Giá trị thực 3', 'Kết luận']]
    for bk in range(len(lst_input)):
        crawler = CrawlerFoodandDrink(lst_input[bk].strip())
        value1 = crawler.get_real_value_1()
        value2 = crawler.get_real_value_2(
            float(lst_lai_suat[bk].strip())) if lai_suat_input else "Nhập lãi suất trái phiếu để tính"
        value3 = crawler.get_real_value_3()
        EPS = crawler.eps
        capital = crawler.capital
        KLDLH = crawler.KLDLH
        rising_speed = crawler.g
        current_price = crawler.get_current_price()
        lai_suat = float(lst_lai_suat[bk].strip()) if lai_suat_input else "Nhập lãi suất trái phiếu để tính",
        result = "Có thể mua" if current_price < value3 else "Nên xem xét"
        summ = [lst_input[bk].upper(), EPS, capital, KLDLH, rising_speed, current_price, lai_suat, value1, value2,
                value3, result]
        lst_re.append(summ)
    lst_re = list(zip(*lst_re))
    return render(request, 'vnidxFootAndDrink/footanddrink.html', {'data': lst_re, 'cpn_code': cpn_code, 'lai_suat': lai_suat_input})
