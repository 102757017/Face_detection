# -*- coding: UTF-8 -*-
import requests
import os
import pprint

os.chdir(os.path.dirname(__file__))


# 创建faceset用来存储face_token
def set_face(outer_id):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id':outer_id
    }
    response = requests.post(url, data=params)
    req_dict = response.json()
    return req_dict

# 查询faceset清单
def get_face():
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
    params = {
        'api_key': key,
        'api_secret': secret,
    }
    response = requests.post(url, data=params)
    req_dict = response.json()
    return req_dict

# 查询指定faceset的内容
def get_detail(outer_id):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id':outer_id
    }
    response = requests.post(url, data=params)
    req_dict = response.json()
    return req_dict

# 删除指定的faceset
def del_face(outer_id):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/delete'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id': outer_id,
        'check_empty':0
    }
    response = requests.post(url, data=params)
    req_dict = response.json()
    return req_dict


key = "kDQHKRtAgO7j1NW31fX7vwiK_msS_Oyi"
secret = "tXF17WS1LeRC7TqaUZWozz-e-Gqqegn8"

if __name__ == "__main__":
    #face_set = set_face('new_set1')
    #print("创建的face_set outer_id为:", face_set['outer_id'])

    face_set = get_face()
    print("查询到的face_set清单如下:")
    pprint.pprint(face_set)

    info=get_detail('new_set1')
    print("查询到的face_set信息如下:")
    pprint.pprint(info)

    del_face('new_set1')
    
    