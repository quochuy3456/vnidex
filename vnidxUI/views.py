from django.shortcuts import render
from vnidxCrawl.views.banks import Crawler

# Create your views here.
def index(request):
    cpn_code = request.GET.get('cpn_code')
    lai_suat = request.GET.get('lai_suat')
    if not cpn_code:
        return render(request, 'vnidxUI/index.html')
    crawler = Crawler(cpn_code)
    context = {
        'value1': crawler.get_real_value_1(),
        'value2': crawler.get_real_value_2(lai_suat) if lai_suat else 0,
        'value3': crawler.get_real_value_3(),
        'EPS': crawler.eps,
        'Capital': crawler.capital,
        'KLDLH': crawler.KLDLH,
        'rising_speed': crawler.g
    }
    return render(request, 'vnidxUI/index.html', context=context)