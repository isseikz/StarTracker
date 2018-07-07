#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import urllib.parse

def urlFromFile(filepath, debug=0):
    tree = ET.parse(filepath)
    root = tree.getroot()

    return addrFrom(root, debug)

def urlFromXml(xml_string, debug=0):
    root = ET.fromstring(xml_string)
    return addrFrom(root, debug)

def addrFrom(root, debug=0):
    if debug>0:
        for child in root:
            print(f'tag: {child.tag}, attribute: {child.attrib}')
            for cchild in child:
                print(f'    tag: {cchild.tag}, attribute: {cchild.attrib}')
                for ccchild in cchild:
                    print(f'        tag: {ccchild.tag}, attribute: {ccchild.attrib}')
                    for cccchild in ccchild:
                        print(f'            tag: {cccchild.tag}, attribute: {cccchild.attrib}')
                        for ccccchild in cccchild:
                            print(f'                tag: {ccccchild.tag}, attribute: {ccccchild.attrib}')
                        pass
                    pass
                pass
            pass
        pass

    deviceInfo = root.find("{urn:schemas-upnp-org:device-1-0}device").find("{urn:schemas-sony-com:av}X_ScalarWebAPI_DeviceInfo")
    uri = urllib.parse.unquote(deviceInfo.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ImagingDevice').find('{urn:schemas-sony-com:av}X_ScalarWebAPI_LiveView_URL').text, 'utf-8')

    for service in deviceInfo.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceList').findall('{urn:schemas-sony-com:av}X_ScalarWebAPI_Service'):
        print(service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType').text)
        if service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ServiceType').text == 'camera':
            camera = urllib.parse.unquote(service.find('{urn:schemas-sony-com:av}X_ScalarWebAPI_ActionList_URL').text).split('/')
            cameraHost = camera[2]
            cameraUrl  = '/' + camera[3] + '/camera'
            print(f'control point: {camera}')

    if debug >0:
        print(f'parsed: {uri}')

    splitted = uri.split('/')

    host = uri.split('/')[2]
    url  = '/'.join(uri.split('/')[3:len(splitted)])

    if debug > 0:
        print(f'host: {host}, url: {url}')


    return uri, host, url, cameraHost, cameraUrl


if __name__ == '__main__':
    urlFromFile('./Qx10Example.xml', 1)
