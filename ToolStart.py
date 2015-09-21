#!/usr/bin/python
#-*- coding: utf-8 -*-

from ToolInit import ProxyServer
import urllib2
import re
import cookielib
import sys

def GetProxyList(URL, page):
    proxyList = []
    # depend on your browser environment
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0"}
    try:
        # post the request to the destination
        request = urllib2.Request(URL, headers=headers)
        # get the data from the destination, you better set the timeout
        response = urllib2.urlopen(request, timeout=10)
        content = response.read()
        print("Bingo, Crawling Successfully!")
        name_ul = re.compile('(?isu)<ul>(.*?)</ul>')
        name_li = re.compile('(?isu)<li[^>]*>(.*?)</li>')
        for row in name_ul.findall(content):
            proxyAddress = ''.join(name_li.findall(row)[0:1])
            proxyHttp = ''.join(name_li.findall(row)[1:2])
            proxySpeed = ''.join(name_li.findall(row)[2:3])
            proxyType  = ''.join(name_li.findall(row)[3:4])
            nameCountry = re.compile('title="(.*?)"')
            proxyCountry = None
            for country in name_li.findall(row)[4:5]:
                proxyCountry = ''.join(nameCountry.findall(country))
                if '&nbsp;' in proxyCountry:
                    proxyCountry = proxyCountry.split('&nbsp;')[0]+' '+proxyCountry.split('&nbsp;')[1]
            proxyServer = ProxyServer(proxyAddress, proxyHttp, proxyType, proxySpeed, proxyCountry)
            proxyList.append(proxyServer)
        print("Successfully Get The Proxy List From Page %d!"%page)
        return proxyList
    except urllib2.HTTPError, error:
        print("Bad, Crawling Unsuccessfully!")
        print(error)
        sys.exit(1)

def FindHighestSpeedProxy(proxyList):
    tempProxy = None
    highestSpeed = 0
    for proxyServer in proxyList:
        if proxyServer.proxy_speed != "-":
            proxyServerSpeed = proxyServer.proxy_speed.split('kbit')[0]
        else:
            proxyServerSpeed = '0'
        # print('ProxyServer.proxy_address = %s'%proxyServer.proxy_address)
        # print('ProxyServer.proxy_speed = %skbit/s'%proxyServer.proxy_speed)
        if float(proxyServerSpeed) > highestSpeed:
            highestSpeed = float(proxyServerSpeed)
            tempProxy = proxyServer
        else:
            pass
    proxyList.remove(tempProxy)
    return tempProxy, proxyList

def ProxySetting(bestProxy):
    try:
        cookiejar = cookielib.LWPCookieJar()
        try:
            cookiesupport = urllib2.HTTPCookieProcessor(cookiejar)
            try:
                proxyHandler = urllib2.ProxyHandler({'http':'http://%s'%bestProxy.proxy_address})
                opener = urllib2.build_opener(proxyHandler, cookiesupport, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                print("Configure Proxy Successfully!")
            except:
                print("Configure Proxy Unsuccessfully!")
        except urllib2.HTTPErrorProcessor, error:
            print("Can Not Process The Cookie!")
            print(error)
            sys.exit(1)
    except cookielib.LoadError, error:
        print("Can Not Load The Cookie!")
        print(error)
        sys.exit(1)

if __name__ == '__main__':
    proxyList = []
    for i in range(10):
        proxyURL = "http://proxy-list.org/english/index.php?p=%s"%str(i+1)
        proxyList += GetProxyList(proxyURL, i+1)
    bestProxy, theRestProxyList = FindHighestSpeedProxy(proxyList)
    bestProxy.ShowInfo()
    # you can crawl whatever you like in the internet!
    ProxySetting(bestProxy)
