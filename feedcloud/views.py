from django.http import HttpResponse
# 目前的 API 视图只能用于接收 POST 请求
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
# 用于返回Json数据
from django.http import JsonResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt

@require_GET
def hello(request):
    with open('templates/index.html', 'rb') as f:
        html = f.read()
    return HttpResponse(html)

@csrf_exempt
@require_POST
def api(request):
    print(request)
    code = request.POST.get('code')
    output = run_code(code);
    return JsonResponse(data={'output':output})

def run_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code], universal_newlines=True, stderr=subprocess.STDOUT, timeout=30)

    except subprocess.CalledProcessError as e:
        output = e.output

    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time Out!!!', e.output])

    return output

code = """print('Test success')"""
print(run_code(code))
