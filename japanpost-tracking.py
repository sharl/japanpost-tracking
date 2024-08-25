# -*- coding: utf-8 -*-
import sys
import time
import io
import binascii
import threading

import schedule
from pystray import Icon, Menu, MenuItem
from PIL import Image
import requests
from bs4 import BeautifulSoup
from win11toast import notify

INTERVAL = 60


class taskTray:
    def __init__(self, code):
        # 追跡番号
        self.code = code
        # 通知済みフラグ
        self.notified = False
        # スレッド実行モード
        self.running = False

        # アイコンの画像をデコード
        self.white = Image.open(io.BytesIO(binascii.unhexlify(WHITE.replace('\n', '').strip())))
        self.red = Image.open(io.BytesIO(binascii.unhexlify(RED.replace('\n', '').strip())))
        menu = Menu(
            MenuItem('Check', self.doCheck),
            MenuItem('Exit', self.stopApp),
        )
        self.app = Icon(name='PYTHON.win32.japanpost', title='japanpost checker', icon=self.white, menu=menu)
        self.doCheck()

    def doCheck(self):
        url = f'https://trackings.post.japanpost.jp/services/srv/search/?requestNo1={self.code}&search=%E9%96%8B%E5%A7%8B&locale=ja'
        r = requests.get(url)
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            title = f'{self.code} 未登録'
            icon = self.white
            st = soup.find_all('table')
            if len(st) >= 2:
                stat = st[1].find_all('tr')[-2].find_all('td')[1].text
                title = f'{self.code} {stat}'
                if stat == 'お届け先にお届け済み':
                    if self.notified is False:
                        self.notified = True
                        notify(
                            body=title,
                            audio='ms-winsoundevent:Notification.Reminder',
                        )
                    icon = self.red

            self.app.title = title
            self.app.icon = icon
            self.app.update_menu()

    def runSchedule(self):
        schedule.every(INTERVAL).seconds.do(self.doCheck)

        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stopApp(self):
        self.running = False
        self.app.stop()

    def runApp(self):
        self.running = True

        task_thread = threading.Thread(target=self.runSchedule)
        task_thread.start()

        self.app.run()


WHITE = """
89504e470d0a1a0a0000000d4948445200000010000000100804000000b5fa37ea0000000467414d410000b18f0bfc6105000000206348524d00007a
26000080840000fa00000080e8000075300000ea6000003a98000017709cba513c00000002624b474400ff878fccbf0000000774494d4507e8081614
123546a9cf91000001044944415428cf8d91bf4ac36014c57f295f9380e01010be0ec5d1c54dfa0e017172f20f9d7c105f210e8eea225debd227e824
f800825068408a98880e9226698ec397c1c152cf72b9f71c2e9c7300100a146ba454952aa51a2956206849649528d76f7c289115c2d163fd85b1ac40
be12ad43221fc5cadcd6a851ad52850aaddc29536c18128198f08261454dc3925dcef0206288e64e7aac0b3dea4d995e75a9237dba1ff30e16a0e480
531e985171c30efb14cea4356e8674d963c2355d3a0cc8f11c8161411f020aee3864c01721b73cd1c6b4304c3981906f66f449595292d163cb09a69e
62ee89e09d676a0c3e3e213db60172ceff11d4c6a8d79575d596b5a9ee1f29e1278a2e34b6a80000002574455874646174653a637265617465003230
32342d30382d32325431313a32303a32392b30393a3030b840d1c50000002574455874646174653a6d6f6469667900323032342d30382d3232543131
3a31383a35332b30393a3030ed9d19db0000000049454e44ae426082
"""

RED = """
89504e470d0a1a0a0000000d4948445200000010000000100803000000282d0f530000000467414d410000b18f0bfc6105000000206348524d00007a
26000080840000fa00000080e8000075300000ea6000003a98000017709cba513c00000174504c5445000000eb6100ec6200ec6100eb6200eb6100eb
6100ec6100ec6200ec6200ec6100ec6200ec6200ec6200ec6200ec6200ec6200eb6100eb6100eb6200eb6200eb6100eb6100ec6100eb6200ec6200ec
6200eb6200ec6200ec6200ec6100eb6200ec6100eb6200eb6100ec6100eb6200ec6200ec6100ec6100eb6200ec6200eb6200eb6100eb6200ec6100ec
6200eb6200eb6100ee6300ed6100eb6000e95f00e75e00e55d00ec6100a746018746198c52298a5530875837855a3b7e5639984307db5b004f342264
686acbcdcfebedefeef0f2e7e9eb808487492b15df5c00ed6200d65700836b5abec0c17b7b7bc9c9c9e8e8e8848484959798755c4ad85800dd5a0087
6852e5e7e97474745f5f5f646464666666b9bbbc7f6552e45d007e573b86888abfc0c0f4f4f5e6e7e7eeeeee8d90914d3625d85900713307575350a2
9d99a19b979a928c948982786c63622f0be25e00d95a00b64d03b24b01b64c01bb4d00c14f00c85200df5d00ef6300ee6200fffffff0e1c3fb000000
2e74524e5300000000000748a7e3fbe348071891eeef18b0b01806919148eda6a6e2fafafae2e2a6499106b018ee9207e3a707046fb7b50000000162
4b47447b4fd2b5fc0000000774494d4507e808161413196d6a9233000000ef4944415418d34d8fd756c25014444f72636240a211d084622f283a5c50
b177418d5d01b1f7ae58b085af37b85cea7e9b97993d442454c84aa5aaba14779548444cf468d5f8a646d3192341afc52f5e9f44febabf1c43bd9f0c
93239ee8eb1f48260711330d0a007c687864746c7c629203410a0153d333b373a9f4fcc22210a230aca5e595d5b5f58dcdad8c85303500d9dc767e67
776fff20033452137078747c727a767e717965a1995a9cb5eb9bdbbbfb87c2e353b9543681e797e2ebdbfbc727b8d95a16e3966ddbf152091c6ded24
7a3afea9eb1231d6a9457ece75f944c1f92b751b8a4b55a33d72af13bf00cbc530522b29a3c60000002574455874646174653a637265617465003230
32342d30382d32325431313a32303a34322b30393a30307c288cb80000002574455874646174653a6d6f6469667900323032342d30382d3232543131
3a31393a32352b30393a30306b4a4ec60000000049454e44ae426082
"""

if __name__ == '__main__':
    if len(sys.argv) == 2:
        code = sys.argv[1].replace('-', '')
        if len(code) == 12 and str(int(code)) == code:
            taskTray(code).runApp()
    else:
        print(f'{sys.argv[0]} <tracking code>')
        exit(1)
