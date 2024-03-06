import requests, json, datetime
import socket
import sys
from httpsig.requests_auth import HTTPSignatureAuth

# 获取token

def get_auth(KeyID, SecretID):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
    return (auth)

#判断资产是否存在
def exist_assest(jms_url,auth,hostname,ip_addr,huanjing):
    url = jms_url + '/api/v1/assets/assets/suggestions/'
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Date': datetime.datetime.utcnow().strftime(gmt_form),
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data_assest = {
        'address': ip_addr
    }
    print(data_assest)
    res = requests.get(url,headers=headers,params=data_assest,auth=auth)
    res_data = res.json()
    print(res_data)
    if len(res_data) >0:
        print(res_data[0].get('ip'))
        print("该资产在之前已经入库，不再入库")
        exit(1)
    else:
        create_assest(jms_url=jms_url,auth=auth,hostname=hostname,ip_addr=ip_addr,huanjing=huanjing)


#推送资产
def create_assest(jms_url,auth,hostname,ip_addr,huanjing):
    url = jms_url + '/api/v1/assets/hosts/'
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Date': datetime.datetime.utcnow().strftime(gmt_form),
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
#http://****/api/docs下node节点的id
    jumpserver_assets_dir = {'shijingshan':'91b356b3-2237-4d3b-a1de-856000d73545','lyzdOps':'acbe7ba8-ac64-4e7f-8a04-cf0bf3e175cd'}

    if huanjing in jumpserver_assets_dir:
        datas = {
                  "name": hostname,
                  "address": ip_addr,
                  "platform": {
                      "id": 1,
                      "name": "Linux"
                    },
                  "nodes": [
                    str(jumpserver_assets_dir[huanjing])
                  ],
                  "protocols": [
                    {
                      "name": "ssh",
                      "port": 22

                    }
                  ],
                  "accounts": [
                    {
                      "name": "default_id_rsa_key",
                      "username": "root",
                      "secret_type": "ssh_key",
                        "source": {
                            "value": "template",
                            "label": "模板"
                        },
                        "source_id": "string",
##jumpserver账号模板ansible的id
                      "template": '72ac7805-c6fc-4398-9409-835025795f8e'
                    }
                  ],
                  "is_active": 'true'
}
    else:
        print("Error:非法的huanjing参数")

    response = requests.post(url, headers=headers,data=json.dumps(datas),auth=auth)
    print("result is: " + response.text)

#获取IP地址
def get_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('1.2.4.8',53))
    ip = s.getsockname()[0]
    s.close()
    return(ip)

if __name__ == '__main__':
    huanjing_arg = ['shijingshan','lyzdOps']
    jms_url = 'http://your_jms_url'
##admin账号的id
    KeyID = 'd543f79a-150d-4ed7-8b45-9a14d3e0f48c'
    SecretID = 'd28ffc39-b2e0-4276-a8de-099c4d042d5c'
    #获取hostname
    hsn = socket.gethostname()
    #获取IP地址
    ip_addr = get_ip_addr()
    hostname =  hsn + '-' + ip_addr.split('.')[-1]
    #获取token
    auth = get_auth(KeyID, SecretID)
    #获取正确的huanjing参数
    if len(sys.argv)!=2:
        print("当前huanjing参数个数为" + str(len(sys.argv)-1) + ",请设置正确的huanjing参数为1个")
        exit(1)
    elif sys.argv[1] not in huanjing_arg:
        print("请设置huanjing参数为shijingshan或lyzdOps!")
        exit(1)
    else:
        huanjing = sys.argv[1]
        exist_assest(jms_url,auth=auth,hostname=hostname,ip_addr=ip_addr,huanjing=huanjing)
