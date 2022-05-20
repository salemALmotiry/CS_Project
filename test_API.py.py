
# from app import db
import requests

# # db.db.create_all()
# BASE = "https://warm-headland-20382.herokuapp.com/"


# API_Key = "Dey7LTaCni98nfhWwefStMUFw6kedmZ5azgT6lX7wuHIeaXWeLf0y3cQDLVo"

#_____________custom________
# key_name = "test3"
# # Generation custom keys
# response = requests.post(BASE+"custom_keys/"+API_Key+"/"+key_name)
# print(response.json())
#end_____________________
#____________get__________
# get custom keys
# response = requests.post(BASE+"getCustomKeys/"+API_Key)
# print(response.json())

#____
# data ={"custom key":"test3"}
# response = requests.post(BASE+"getPublic/"+API_Key,data=data)
# print(response.json())

#___________en__________


# file = {'file': open('RSA.pdf', 'rb')}

# response = requests.post(BASE+"encrypt/"+API_Key,files=file,)
# if response.status_code == 200:
#     with open("en.pdf", 'wb') as f:
#         f.write(response.content)
#end__________________________

#_____________de_____________
# file = {'file': open('en.pdf', 'rb')}

# response = requests.post(BASE+"decrypt/"+API_Key,files=file,)
# if response.status_code == 200:
#     with open("de.pdf", 'wb') as f:
#         f.write(response.content)
#end___________________________

#_____________sign_____________


# file = {'file': open('en.pdf', 'rb')}
# response = requests.post(BASE+"sign/"+API_Key,files=file)
# if response.status_code == 200:
#         with open("sign.txt", 'wb') as f:
#             f.write(response.content)

#end___________________________________

#_____________ver_____________

# file = {'file': open('en.pdf', 'rb') ,
#     'file2': open('sign.txt', 'rb') }

# response = requests.post(BASE+"verify/"+API_Key,files=file)
# print(response.json())

#end___________________________




# _________________________________________


# key='''-----BEGIN RSA PUBLIC KEY-----
# MIGJAoGBAIBWCiHJOaIWVqjpO48Eek2HbCE7ZtyjFjGaCBIdLrOOocpJeVJqiB99
# G2EF1rQcC+d9scBjUsB/jU/fXa9Mv7ryKr2Ew8O4FyW9QZOvgntV+61mpQI9OWZf
# xbznnS7euaBfZBkh+f8jmi6eUx2nF2HrY/4O11LNIjymOt7yfqaBAgMBAAE=
# -----END RSA PUBLIC KEY-----'''
# data = {"key name":"salem",
#         "key data":key}

# response = requests.post(BASE+"add_key/"+API_Key,data=data)

