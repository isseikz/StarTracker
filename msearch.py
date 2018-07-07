# -*- coding:utf-8 -*-

# PythonでUPnPによるポートマップ(なぜなに Torrent)
# https://symfoware.blog.fc2.com/blog-entry-1990.html

import socket
import urllib.request
import urllib.parse as urlparse
import json

import xmlParser

def urlLiveview():
    host = '239.255.255.250'
    port = 1900
    messages = [
        b'M-SEARCH * HTTP/1.1',
        b'HOST: 239.255.255.250:1900',
        b'MAN: "ssdp:discover"',
        b'MX:1',
        b'ST: urn:schemas-sony-com:service:ScalarWebAPI:1',
    ]
    # messages = [
    #     b'M-SEARCH * HTTP/1.1',
    #     b'MX: 3',
    #     b'HOST: 239.255.255.250:1900',
    #     b'MAN: "ssdp:discover"',
    #     b'ST: urn:schemas-upnp-org:service:WANIPConnection:1',
    # ]
    message = b'\r\n'.join(messages)
    message += b'\r\n\r\n' # 末尾に改行コードを2つ付与
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (host, port))
    res = sock.recv(4096)
    # print(res)
    sock.close()

    for line in str(res).split('\\r\\n'):
        print(line)
        info = line.strip()
        if not info.startswith('LOCATION:'):
            continue

        locaction = info[len('LOCATION:'):].strip()
        print(f'locaction: {locaction}')
        break


    # --- XMLの解析
    f = urllib.request.urlopen(locaction)
    xml_string = f.read()
    f.close()

    uri, host, url, cameraHost, cameraUrl = xmlParser.urlFromXml(xml_string, 1)

    return uri, host, url, cameraHost, cameraUrl




if __name__ == '__main__':
    urlLiveview()
