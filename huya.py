from bs4 import BeautifulSoup
import requests
import json

def huya(url:str) -> str:
    #get content from url with user-agent and store in htmlDoc
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    htmlDoc = requests.get(url, headers=headers)
    #parse htmlDoc with BeautifulSoup
    soup = BeautifulSoup(htmlDoc.text, 'html.parser')
    a = soup.body.contents[8]
    #replace '<script> window.HNF_GLOBAL_INIT = ' with empty string
    b = str(a).replace('<script> window.HNF_GLOBAL_INIT = ', '')
    #replace '</script>' with empty string
    c = str(b).replace('</script>', '')
    #get the json content and decode it
    jsonContent = json.loads(c)
    #get the roomValue from the json content
    roomValue = jsonContent['roomInfo']['tLiveInfo']['tLiveStreamInfo']['vStreamInfo']['value']

    #create a loop to store all cdnType into a list
    cdnTypeList = []
    for i in range(0, 3):
        cdnType = roomValue[int(i)]['sCdnType']     
        #store cdnType in cdnTypeList
        cdnTypeList.append(str(i) + cdnType)

    #ask user to input the cdn number
    cdnNumber = (input(str(cdnTypeList) + 'Please input the cdn type number: '))
    #get parameter
    sStreamName = roomValue[int(cdnNumber)]['sStreamName']
    sFlvUrl = roomValue[int(cdnNumber)]['sFlvUrl']
    sFlvAntiCode = roomValue[int(cdnNumber)]['sFlvAntiCode']
    
    #conbine the url
    finalUrl = sFlvUrl + '/' + sStreamName + '.flv?' + sFlvAntiCode
    
    return finalUrl

print(huya('https://m.huya.com/243547'))