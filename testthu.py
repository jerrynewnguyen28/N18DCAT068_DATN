# start_index = 127
# end_string = '\x00\x17'
# # print(end_string.encode())

# a = b'\x16\x03\x01\x02\x00\x01\x00\x01\xfc\x03\x03\xde2\xbc\x99\xcf\x07z\xe0(\xbe7C\x98\x90\xd5\xfct\x8c.\xe8\x1b\x11MY\xec\x7f\xc8\xae4\x80\xdfi \xd0\x8c}{\x90\xc3y\xe0r\xe2\xf6k\x1f\x8d\xe4\xd4\xa0\x9d\xa6Z\xdf\x16\x12\xc5\xa9w\x9e\xe6\xd1\xfbh\xc3\x00 \x1a\x1a\x13\x01\x13\x02\x13\x03\xc0+\xc0/\xc0,\xc00\xcc\xa9\xcc\xa8\xc0\x13\xc0\x14\x00\x9c\x00\x9d\x00/\x005\x01\x00\x01\x93\xaa\xaa\x00\x00\x00\x00\x00\x15\x00\x13\x00\x00\x10ads.pubmatic.com\x00\x17\x00\x00\xff\x01\x00\x01\x00\x00\n\x00\n\x00\x08zz\x00\x1d\x00\x17\x00\x18\x00\x0b\x00\x02\x01\x00\x00#\x00\x00\x00\x10\x00\x0e\x00\x0c\x02h2\x08http/1.1\x00\x05\x00\x05\x01\x00\x00\x00\x00\x00\r\x00\x12\x00\x10\x04\x03\x08\x04\x04\x01\x05\x03\x08\x05\x05\x01\x08\x06\x06\x01\x00\x12\x00\x00\x003\x00+\x00)zz\x00\x01\x00\x00\x1d\x00 X.\x87D\x1f\xb6 \xaag|\x16\xca\x1d\\\xa0}\xf6\xb3\x96\xe7\xb5[\xd97\xbe\xc2m\xe8\xd0\xa8iW\x00-\x00\x02\x01\x01\x00+\x00\x07\x06::\x03\x04\x03\x03\x00\x1b\x00\x03\x02\x00\x02Di\x00\x05\x00\x03\x02h2\n\n\x00\x01\x00\x00\x15\x00\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# end_index = a.find(end_string.encode(),start_index)
# url = a[start_index:end_index]
# haha = url.decode('utf-8', 'backslashreplace')
# print(end_index)
# # print(a[0:127])
# print(url)
# print(haha)
import pydivert
import re
def extract_url_https(payload_tcp):
    start_index = 127
    end_string = '\x00\x17'
    end_index = payload_tcp.find(end_string.encode(),start_index)
    url = payload_tcp[start_index:end_index]
    if len(url)!=0 and check_Format_of_URL(url.decode('utf-8', 'backslashreplace')):
        url = url.decode('utf-8', 'backslashreplace')
        return url
    return "1"
def extract_url(payload_tcp, dst_port):
    if dst_port == 80:
        return extract_url_http(payload_tcp)
    if dst_port == 443:
        return extract_url_https(payload_tcp)


def extract_url_http(payload_tcp):
    start_string='Host: '
    end_string = '\r\nConnection'
    start_index = payload_tcp.find(start_string.encode())
    end_index = payload_tcp.find(end_string.encode())
    host = payload_tcp[start_index+6:end_index]

    start_string = 'GET '
    end_string= ' HTTP'
    start_index = payload_tcp.find(start_string.encode())
    end_index = payload_tcp.find(end_string.encode())
    path = payload_tcp[start_index+4:end_index]
    # print("hostname: ",host," path: ",path)
    url = host + path
    if len(url)!=0 and check_Format_of_URL(url.decode()):
        url = url.decode()
        return url
    return ""



def check_Format_of_URL(url):
    regex = r"(?i)\b(^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$)"
    return re.compile(regex).match(url)
with pydivert.WinDivert("tcp.DstPort == 443 and tcp.PayloadLength > 0") as w:
                for packet in w:
                    payload_tcp = packet.tcp.payload
                    dst_port = packet.dst_port
                    print(packet.tcp.payload)
                    url_name = extract_url(payload_tcp,dst_port)
                    print(url_name)
                    w.send(packet)               
# Capture only TCP packets to port 80, i.e. HTTP requests.
# w = pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0")

# w.open()  # packets will be captured from now on

# packet = w.recv()  
# payload_tcp = packet.tcp.payload
# dst_port = packet.dst_port
# haha = extract_url(payload_tcp,dst_port)
# print(haha)
# w.send(packet)  # re-inject the packet into the network stack
# deny_url = []
# deny_url.append("a")
# deny_url.append("b")
# deny_url.append("c")
# deny_url.append("d")

# for i in range(len(deny_url)):
#     print(deny_url[i])
# deny_url.remove("c")
# print("============ remove C = > len", len(deny_url))
# for i in range(len(deny_url)):
#     print(deny_url[i])    
# deny_url.remove("b")
# print("============ remove B = > len", len(deny_url))
# for i in range(len(deny_url)):
#     print(deny_url[i])

        
        
# w.close()  # stop capturing packets