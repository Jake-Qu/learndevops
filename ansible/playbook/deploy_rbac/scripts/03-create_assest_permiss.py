import requests, json, datetime
import sys
from httpsig.requests_auth import HTTPSignatureAuth



def get_auth(KeyID, SecretID):
  signature_headers = ['(request-target)', 'accept', 'date']
  auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
  return (auth)


#获取用户uuid
def get_user_uuid(jms_url, auth, yonghu):
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
  res = requests.get(url, headers=headers, params=data_assest, auth=auth)
  res_data = res.json()
  if len(res_data) <= 0:
    print("用户" + res_data[0].get('username') + "不存在")
    exit(1)
  else:
    return (res_data[0]['id'])
    # create_user(jms_url=jms_url, auth=auth, yonghu=yonghu)

def create_user(jms_url, auth, yonghu):
  url = jms_url + '/api/v1/perms/asset-permissions/'
  gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
  user_uid = get_user_uuid(jms_url, auth, yonghu)
  headers = {
    'Date': datetime.datetime.utcnow().strftime(gmt_form),
    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }

  datas = {
    "name": str(yonghu) + "资产授权",
    "users": [
        str(user_uid)
    ],
    "assets": [
      "1f98a42e-7501-461a-97dc-143f2e8cde02"
    ],
    "accounts": [
      str(yonghu)
    ],
    "actions": [
        {
          "value": "connect",
          "label": "连接 (所有协议)"
        },
        {
          "value": "upload",
          "label": "上传 (RDP, SFTP)"
        },
        {
          "value": "download",
          "label": "下载 (RDP, SFTP)"
        },
        {
          "value": "copy",
          "label": "复制 (RDP, VNC)"
        },
        {
          "value": "paste",
          "label": "粘贴 (RDP, VNC)"
        },
        {
          "value": "delete",
          "label": "删除 (SFTP)"
        }
      ],
    "is_active": 'true',
    "date_start": "2023-08-30T07:34:37.545Z",
    "date_expired": "2099-08-30T07:34:37.545Z"
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
        create_user(jms_url, auth=auth, yonghu=yonghu)