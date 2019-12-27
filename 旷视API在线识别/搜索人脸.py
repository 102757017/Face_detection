# -*- coding: UTF-8 -*-
import requests
import os
import pprint
import cv2
import numpy as np

os.chdir(os.path.dirname(__file__))


# 检测图片中的人脸（支持一至多张人脸），获取人脸位置及face_token。对于试用 API Key，最多只对人脸框面积最大的 5 个人脸进行分析
# 如果对同一张图片进行多次人脸检测，同一个人脸得到的 face_token 是不同的
# 此API只支持jpg，png格式的照片识别，图片像素尺寸：最小 48*48 像素，最大 4096*4096 像素，图片文件大小：2 MB
def detect_face(filepath):
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
    if os.path.getsize(filepath) > 2 * 1024 * 1024:
        print("图片大小超出限制")
        exit(0)
    if img.shape[0] > 4096 or img.shape[1] > 4096:
        print("图片分辨率超出限制")
        exit(0)
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key": key, "api_secret": secret}
    response = requests.post(http_url, data=data, files=files)
    req_dict = response.json()
    pprint.pprint(req_dict)
    return req_dict


def creat_set(outer_id):  # 创建faceset用来存储face_token
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id': outer_id  # 自定义标识，可以用来管理 FaceSet 对象。最长255个字符，不能包括字符^@,&=*'"
    }
    response = requests.post(url, data=params)
    req_dict = response.json()
    return req_dict


# 将facetokens保存到faceset中，如果一个 face_token 在 72 小时内没有存放在任一 FaceSet 中，则该 face_token 将会失效
def addface(outer_id, facetokens):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id': outer_id,  # face_set对应的outer_id
        'face_tokens': facetokens
    }
    r = requests.post(url, data=params)
    req_dict = r.json()
    pprint.pprint(req_dict)


def removeface(outer_id, facetokens):  # 移除一个FaceSet中的某些或者全部face_token
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id': outer_id,  # face_set对应的outer_id
        'face_tokens': facetokens
    }
    r = requests.post(url, data=params)
    req_dict = r.json()
    pprint.pprint(req_dict)


key = "kDQHKRtAgO7j1NW31fX7vwiK_msS_Oyi"
secret = "tXF17WS1LeRC7TqaUZWozz-e-Gqqegn8"


# 为之前已经写进face_set中的face_token添加user_id,这里userid是一个字符串，我们在这里可以备注图片的姓名等其他信息 。该信息会在Search接口结果中返回，用来确定用户身份。
def face_SetUserID(face_token, user_id):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'
    params = {
        'api_key': key,
        'api_secret': secret,
        'face_token': face_token,
        'user_id': user_id
    }
    r = requests.post(url, data=params)
    req_dict = r.json()
    print(req_dict)
    return req_dict


def face_search(image_file1, outer_id):  # 在指定的face_set中搜索人脸
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    files = {"image_file": open(image_file1, "rb")}
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id': outer_id,  # face_set对应的唯一标识
    }
    r = requests.post(url, files=files, data=params)
    req_dict = r.json()
    pprint.pprint(req_dict)
    return req_dict


if __name__ == "__main__":
    filepath = "example.jpg"
    data = detect_face(filepath)
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
    for r in data["faces"]:
        x0 = r["face_rectangle"]['left']
        y0 = r["face_rectangle"]['top']
        x1 = r["face_rectangle"]['width']+x0
        y1 = r["face_rectangle"]['height']+y0
        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 1)  # 12
        print("该人脸的face_id（唯一识别码）是", r["face_token"])
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # creat_set(outer_id='new_set1')
    # addface(outer_id='new_set1',facetokens=r["face_token"])
    # face_SetUserID(face_token=r["face_token"],user_id="马云")
    result = face_search(image_file1=filepath,
                         outer_id='new_set1')
    print("该照片内的人脸是:", result['results'][0]['user_id'])
    print("置信度是:", result['results'][0]['confidence'])
    if result['results'][0]['confidence'] > result['thresholds']['1e-5']:
        print('识别的结果十分可靠')
    else:
        print('识别的结果不太可靠')
