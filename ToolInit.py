#!/usr/bin/python
#-*- coding: utf-8 -*-

class ProxyServer:
    def __init__(self, proxy_address, proxy_http, proxy_type, proxy_speed, proxy_country):
        self.proxy_address = proxy_address
        self.proxy_http = proxy_http
        self.proxy_type = proxy_type
        self.proxy_speed = proxy_speed
        self.proxy_country = proxy_country
    def ShowInfo(self):
        print('*'*40)
        print("*Address: %s"%self.proxy_address+" "*(29-len(self.proxy_address))+"*")
        print("*Http: %s"%self.proxy_http+" "*(32-len(self.proxy_http))+"*")
        print("*Type: %s"%self.proxy_type+" "*(32-len(self.proxy_type))+"*")
        print("*Speed: %s"%self.proxy_speed+"/s"+" "*(29-len(self.proxy_speed))+"*")
        print("*Country: %s"%self.proxy_country+" "*(29-len(self.proxy_country))+"*")
        print('*'*40)
