import json
from typing import *

import requests
from bs4 import BeautifulSoup


def huyaNew(room_id: str) -> str:
    try:
        if not room_id.isdigit():
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
                htmlDoc = requests.get(
                    f'https://m.huya.com/{room_id}', headers=headers)
                soup = BeautifulSoup(htmlDoc.text, 'html.parser')
                a = soup.body.contents[8]
                b = str(a).replace('<script> window.HNF_GLOBAL_INIT = ', '')
                c = str(b).replace('</script>', '')
                jsonContent = json.loads(c)
                room_id = str(jsonContent['roomInfo']
                              ['tProfileInfo']['lProfileRoom'])
                print(
                    f'Your room id is invalid! The real room id is: {room_id}')
            except:
                print('Room id is invalid!')
                return
        api_url = 'https://mp.huya.com/cache.php?m=Live&do=profileRoom&roomid='
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        html = requests.get(api_url + room_id, headers=headers)
        data = json.loads(html.text)['data']

        nick = data['profileInfo']['nick']
        room_name = data['liveData']['roomName']
        liveStatus = data['liveStatus']
    except:
        print('Room id is invalid!')
        return
    

    if liveStatus == "OFF":
        return f'{room_name} {nick} is offline'
    else:
        stream_dict = data['stream']
        flv = stream_dict['flv']  # type: dict
        cdn = flv['multiLine']  # type: List
        rate = flv['rateArray']  # type: List
        supportable_resolution = {'原画': '', }
        for b in rate:
            supportable_resolution[b['sDisplayName']] = b['iBitRate']
        sort_dict = {}
        for resolution, bitrate in supportable_resolution.items():
            print(f'{resolution} {bitrate}')
            url_list = []
            for i in cdn:
                url = i['url'].replace('http://', 'https://')  # type: str
                url = url.replace(
                    'imgplus.flv', f'imgplus_{bitrate}.flv')  # type: str
                url_list.append(url)

            sort_dict[resolution] = url_list
        display = ''
        for resolution, url_list in sort_dict.items():
            display += f'{resolution}:\n'
            for i in url_list:
                display += f'{i}\n'
    return f'{nick} is online \n{room_name} \n{display}'


if __name__ == '__main__':
    room_id = input('Please input the room id: ')
    if room_id == '':
        print(huyaNew('243547'))
    print(huyaNew(room_id))
