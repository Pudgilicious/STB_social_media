from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list

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
