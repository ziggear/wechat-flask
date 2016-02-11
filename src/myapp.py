# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

from flask import Flask
from flask import request
import hashlib, time
import xml.etree.ElementTree as ET

app = Flask(__name__)

wechat_token = 'james_is_god'

# 检查签名正确性的
def check_signature(signature, timestamp, nonce):
    token = wechat_token
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = tmp_arr[0] + tmp_arr[1] + tmp_arr[2]
    sha1_tmp_str = hashlib.sha1(tmp_str).hexdigest()
    if (sha1_tmp_str == signature) :
        return True
    else :
        return False

@app.route('/')
def hello_world():
    return 'Hello Wechat!'

@app.route('/wechat/', methods=['GET', 'POST'])
def respond():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    if request.method == 'GET':
        if check_signature(signature, timestamp, nonce) :
            return echostr
        else :
            return 'Not Valid!'
    else :
        # if check_signature(signature, timestamp, nonce) :
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        re_msg = (reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        return re_msg

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=2000)
