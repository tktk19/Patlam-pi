# はじめに
## Raspberry Piへのログイン方法 及び rootになる方法
   下記でログインしてください
   
   IPアドレス : 発声通知されたもの
   ポート     : 10022
   User      : pi
   Pass      : 1qazse4
    # ssh -p 10022 pi@[通知されたIP]

   root になるためには下記
    # sudo su -   
   
## 設定ミス等で通信できなくなってしまった場合
   hdmiケーブルにてTVに接続の上
   USBキーボードを取り付ける事で、通常のLinuxマシンとなります
   この状態で再設定を行って下さい、システムの復元が必要な場合には
   下記にURLを書いておりますので、そちらもご利用下さい。

## 備考
   WDTが有効化されているため、LoadAverageが一定以上になると
   強制的に再起動がかかります

## テスト Linuxマシンよりsnmpコマンドを叩いて下さい
    # sudo snmptrap -v 2c -c public [設定したIPアドレス] '' .1.3.6.1.4.1.8072.99999 .1.3.6.1.4.1.8072.99999.1 s "Hello World"
    
## 注意事項
   音声の発声部分に個人非営利利用無償の aquestalkpi を利用しています
   http://www.a-quest.com/products/aquestalkpi.html

# 設置手順
## 物理的に設置
1. スピーカーをUSBポートに刺す
2. LED用コネクタを docs/raspP1.png の [20(GND), 18, 16] に接続
3. SDカードを刺す
   SDカード破損やDHCP接続に戻したい場合には 下記よりダウンロード
   http://kouzu.info/sd/RaspbianWithPatlam-pi.dmg
4. micro-USBコネクタにて電源供給
5. 起動後にIPアドレスが音声通知されます
6. http://[通知されたIP]/ をブラウザにて開く

## IPアドレスの変更
1. RaspberryPiへログイン
2. /etc/network 配下にある dhcp用 / static用のいずれかを利用下さい
   DHCP利用の場合
   # cp /etc/network/interfaces_dhcp /etc/network/interfaces
   
   Staticの場合 ファイルを編集後コピーして下さい
   # vi /etc/network/interfaces_static
   # cp /etc/network/interfaces_static /etc/network/interfaces
   
   設定後は再起動を実施して下さい
   # shutdown -r now
   失敗した際には焦らずに上記の [設定ミス等で通信できなくなってしまった場合] を実施