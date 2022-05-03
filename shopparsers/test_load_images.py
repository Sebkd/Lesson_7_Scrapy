# '''
# Тестовая инсталляция загрузки картинок по url
# '''
# import requests
#
# response = requests.get('https://73.img.avito.st/640x480/13560600873.jpg')
#
# with open('./../static/img/avito.jpg', 'wb+') as f:
#     f.write(response.content)

'''
Тестовая инсталляция загрузок картинок с использованием wget
'''

import requests
import wget

url = 'https://73.img.avito.st/640x480/13560600873.jpg'

wget.download(url, out='./../static/img/')