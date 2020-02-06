from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list


a = [proxies[i].get_address() for i in range(len(proxies))]
ip_list = a[1:10]

from selenium import webdriver

PROXY = proxies[0].get_address()
webdriver.DesiredCapabilities.CHROME['proxy']={
    
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    
    "proxyType":"MANUAL",
    
}
driver = webdriver.Chrome("./chromedriver")
driver.get("ctrip.com")


def proxy_check_simple(proxies):
    import requests
    from requests.exceptions import ConnectionError, ProxyError
    good_proxies = []
    proxy_list = []
    def check(proxy):
        try:
            response = requests.get("https://ipapi.co/json/", proxies = proxy, timeout = 10)
            good_proxies.append(proxy)
            print(str(proxy) + " is good.")
        except ProxyError:
            print(str(proxy) + " is not responding.")
        except ConnectionError:
            print(str(proxy) + " connection denied.")
        except:
            print(str(proxy) + " exceeded timeout or other errors.")
    count = 0
    for proxy in proxies:
        check(proxy)
        count += 1
        print(str(count) + '/' + str(len(proxies)) + ' tested.')
        if len(good_proxies) == 20:
            break
        # if count == 11:
        #     break
    return good_proxies


import urllib.request
import socket
import urllib.error

def is_bad_proxy(pip):    
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://www.example.com')  # change the URL to test here
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False

def main():
    socket.setdefaulttimeout(120)

    # two sample proxy IPs
    #proxyList = ['125.76.226.9:80', '25.176.126.9:80']
    proxyList = ip_list

    for currentProxy in proxyList:
        if is_bad_proxy(currentProxy):
            print("Bad Proxy %s" % (currentProxy))
        else:
            print("%s is working" % (currentProxy))

if __name__ == '__main__':
    main() 