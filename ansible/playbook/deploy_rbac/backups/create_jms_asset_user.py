import requests, json, datetime
import socket
import sys
from httpsig.requests_auth import HTTPSignatureAuth


def get_auth(KeyID, SecretID):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
    return (auth)


def exist_account(jms_url,auth,yonghu):
    url = jms_url + '/api/v1/accounts/accounts/'
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Date': datetime.datetime.utcnow().strftime(gmt_form),
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data_assest = {
        'asset_id': '1f98a42e-7501-461a-97dc-143f2e8cde02',
        'username': str(yonghu)
    }
    print(data_assest)
    res = requests.get(url, headers=headers,params=data_assest,auth=auth)
    res_data = res.json()
    if len(res_data) >0:
        print(res_data[0].get('username'))
        print("用户"+ res_data[0].get('username') +"在之前已经入库到10.1.128.103，不再入库")
        exit(1)
    else:
        create_account(jms_url=jms_url,auth=auth,yonghu=yonghu)

#推送资产
def create_account(jms_url,auth,yonghu):
    url = jms_url + '/api/v1/accounts/accounts/'
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
  "secret_type": {
    "value": "password",
    "label": "密码"
  },
  "secret": "Welcome1*",
  "su_from": "0dc547d8-18e9-485c-8e8a-c407ef626c84",
  "asset": {
    "id": "1f98a42e-7501-461a-97dc-143f2e8cde02",
    "name": "sit_k8s_master_node3",
    "address": "10.1.128.103"
  },
  "version": 0,
  "source": {
    "value": "local",
    "label": "数据库"
  },
  "params": {},
  "on_invalid": {
    "value": "error",
    "label": "失败"
  },
  "privileged": 'false',
  "is_active": 'true',
  "push_now": 'false'
}
    response = requests.post(url, headers=headers, data=json.dumps(datas), auth=auth)
    print("result is: " + response.text)

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
        exist_account(jms_url, auth=auth, yonghu=yonghu)
