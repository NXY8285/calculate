import json
import logging
import requests

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import *


logger = logging.getLogger('log')


# def index(request, _):
#     """
#     获取主页

#      `` request `` 请求对象
#     """

#     return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    # rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    # if request.method == 'GET' or request.method == 'get':
        # rsp = get_count()
    if request.method == 'POST' or request.method == 'post':
        rsp=get_img_id(request)
    #     # rsp = update_count(request)
    #     rsp = update_count(request)
    # else:
    #     rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
    #                         json_dumps_params={'ensure_ascii': False})
    # logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp

def get_img_id(request):
    # try:
    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    filepath=body['filepath']
    # 实际地址有变，需从前端传
    # path="https://7072-prod-8g7lbzqkeb6ed463-1314085351.tcb.qcloud.la/my-photo.png?sign=cfd46cb0533896aaa3aa89869e1fd86e&t=1668011602"
    # "cloud://prod-8g7lbzqkeb6ed463.7072-prod-8g7lbzqkeb6ed463-1314085351/my-photo.png"
   
    # 需要管理员获得密钥
    response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxe29e8979302727fb&secret=b6d8d35653a2905bced39262b933da83',)
    
    data ={
        "env": "prod-8g7lbzqkeb6ed463",
        "path": "result.jpg"
    }
    #转json
    data = json.dumps(data) #一定要把参数转为json格式，不然会请求失败
    response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data)
    logger.info(response.json())
    
    result=main(filepath, False)
    
    data2={
        "Content-Type":(None,".jpg"), #此处为上传文件类型
        "key": (None,"result.jpg"),
        "Signature": (None,response.json()['authorization']),
        'x-cos-security-token': (None,response.json()['token']),
        'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
        'file': ('result.jpg',result)
    }
    response2 = requests.post(response.json()['url'], files=data2) #此处files提交的为表单数据，不为json数据，json数据或其他数据会报错
    # print(response2)

    logger.info(response2)

# def get_count():
#     """
#     获取当前计数
#     """

#     try:
#         data = Counters.objects.get(id=1)
#     except Counters.DoesNotExist:
#         return JsonResponse({'code': 0, 'data': 0},
#                     json_dumps_params={'ensure_ascii': False})
#     return JsonResponse({'code': 0, 'data': data.count},
#                         json_dumps_params={'ensure_ascii': False})


# def update_count(request):
#     """
#     更新计数，自增或者清零

#     `` request `` 请求对象
#     """

#     logger.info('update_count req: {}'.format(request.body))

#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)

#     if 'action' not in body:
#         return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
#                             json_dumps_params={'ensure_ascii': False})

#     if body['action'] == 'inc':
#         try:
#             data = Counters.objects.get(id=1)
#         except Counters.DoesNotExist:
#             data = Counters()
#         data.id = 1
#         data.count += 1
#         data.save()
#         return JsonResponse({'code': 0, "data": data.count},
#                     json_dumps_params={'ensure_ascii': False})
#     elif body['action'] == 'clear':
#         try:
#             data = Counters.objects.get(id=1)
#             data.delete()
#         except Counters.DoesNotExist:
#             logger.info('record not exist')
#         return JsonResponse({'code': 0, 'data': 0},
#                     json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
#                     json_dumps_params={'ensure_ascii': False})
