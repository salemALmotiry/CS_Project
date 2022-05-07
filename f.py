

import requests

BASE = "https://warm-headland-20382.herokuapp.com/"
username = "tes3t"
password = "t32st"
API_Key = "vLwwc4u59h3wbwLDhPlCLRj4iTOixEXx0NxqQiyukIUr-WWwYTpemulp43gj"


# response = requests.get(BASE+"api/"+username+"/"+password)
# print(response.json())
# ___________________



                
# response = requests.get(BASE+"getPublic/"+API_Key)
# print(response.json())

# response1 = requests.get(BASE+"getPrivate/"+API_Key)
# print(response.json())


# __________________________________________


# file = {'file': open('text.docx', 'rb')}

# response = requests.post(BASE+"encrypt/"+API_Key,files=file)
# if response.status_code == 200:
#     with open("en.docx", 'wb') as f:
#         f.write(response.content)

#_____________________________________________________-



# file = {'file': open('en.docx', 'rb')}

# response = requests.post(BASE+"decrypt/"+API_Key,files=file)
# if response.status_code == 200:
#   with open("de.docx", 'wb') as f:
#       f.write(response.content)

# ___________________________________________

# file = {'file': open('en.docx', 'rb')}

# response = requests.post(BASE+"sign/"+API_Key,files=file)
# if response.status_code == 200:
#         with open("sign.txt", 'wb') as f:
#             f.write(response.content)


# _________________________________________

# file = {'file': open('en.docx', 'rb') ,
#     'file2': open('sign.txt', 'rb') }
# response = requests.post(BASE+"verify/"+API_Key,files=file)
# print(response.json())