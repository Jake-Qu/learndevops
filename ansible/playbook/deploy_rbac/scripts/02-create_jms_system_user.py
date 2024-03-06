import requests, json, datetime
import sys
from httpsig.requests_auth import HTTPSignatureAuth
import random
def get_auth(KeyID, SecretID):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
    return (auth)

def exist_user(jms_url,auth,yonghu):
    url = jms_url + '/api/v1/users/users/'
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Date': datetime.datetime.utcnow().strftime(gmt_form),
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data_assest = {
        'username': str(yonghu)
    }
    res = requests.get(url, headers=headers,params=data_assest,auth=auth)
    res_data = res.json()
    if len(res_data) >0:
        print(res_data[0].get('username'))
        print("用户"+ res_data[0].get('username') +"在之前已经入库到JumpServer，不再入库")
        exit(1)
    else:
        create_user(jms_url=jms_url,auth=auth,yonghu=yonghu)

def create_user(jms_url,auth,yonghu):

    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    str1 = []
    for i in range(16):
        str1.append(random.choice(seed))
    StringS = ''.join(str1)


    url = jms_url + '/api/v1/users/users/'
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Date': datetime.datetime.utcnow().strftime(gmt_form),
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    datas = {
  "name": str(yonghu),
  "username": str(yonghu),
  "password": str(StringS),
  "public_key": "",
  "email": str(yonghu)+"@lyzdfintech.com",
  "mfa_level": {
    "value": 0,
    "label": "禁用"
  },
  "source": {
    "value": "local",
    "label": "数据库"
  },
  "password_strategy": "custom",
  "is_service_account": 'false',
  "is_active": 'true',
  "need_update_password": 'true',
  "date_expired": "2099-08-30T06:23:18.085Z"
}
    response = requests.post(url, headers=headers, data=json.dumps(datas), auth=auth)
    print("请管理员登录jumpserver 重置密码给用户")
    print("创建用户: "+ str(yonghu))
    print("密码： "+ str(StringS))
    # print("result is: " + response.text)

if __name__ == '__main__':
    jms_url = 'http://10.1.128.53'
    KeyID = 'b1316e1d-b23d-405c-b6d0-177cab125155'
    SecretID = '6167cae4-3847-4045-a8f5-0fa40b46a088'

    #获取token
    auth = get_auth(KeyID, SecretID)
    # 获取正确的yonghu参数
    if len(sys.argv) != 2:
        print("当前yonghu参数个数为" + str(len(sys.argv) - 1) + ",请设置正确的yonghu参数为1个")
        exit(1)
    else:
        yonghu = sys.argv[1]
        # create_account(jms_url, auth=auth, yonghu=yonghu)
        exist_user(jms_url, auth=auth, yonghu=yonghu)