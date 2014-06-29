# 設置手順
## 物理的に設置
1. micro-USBコネクタに電源共有
2. スピーカーを全面のUSBポートに






# RaspberryPi Linuxへの変更点
下記は既に設定済みの内容のメモとなります

## InstallPackages
    snmp
    watchdog
    chkconfig

## SNMP
### /etc/default/snmpd  
    $ diff snmpd snmpd.org
    16c16
    < TRAPDRUN=yes
    ---
    > TRAPDRUN=no

### /etc/snmp/snmpd.conf  
    #       sec.name  source          community
    com2sec notConfigUser  default       public

    #       groupName      securityModel securityName
    group   notConfigGroup v1           notConfigUser
    group   notConfigGroup v2c           notConfigUser

    #       name           incl/excl     subtree         mask(optional)
    view    systemview    included   .1.3.6.1.2.1.1
    view    systemview    included   .1.3.6.1.2.1.25.1.1

    #       group          context sec.model sec.level prefix read   write  notif
    access  notConfigGroup ""      any       noauth    exact  systemview none none

### /etc/snmp/snmptrapd.conf  
    #### When Recieve Trap
    #default : write to syslog
    traphandle default /usr/bin/logger

    #### Settings
    doNotRetainNotificationLogs yes
    doNotLogTraps no
    doNotFork no

    # authCommunity   TYPES COMMUNITY   [SOURCE [OID | -v VIEW ]]
    #authCommunity     log   "community" 192.168.1.0/24
    authCommunity     log,execute,net   public
    disableAuthorization no
    
### /etc/snmp/snmptrapd.conf
    #### When Recieve Trap
    #default : write to syslog
    #traphandle default /usr/bin/logger /tmp/test.log
    traphandle default /prj/Patlam-pi/bin/trap_receive.py
    
    #### Settings
    doNotRetainNotificationLogs yes
    doNotLogTraps no
    doNotFork no
    
    # authCommunity   TYPES COMMUNITY   [SOURCE [OID | -v VIEW ]]
    authCommunity     log,execute,net   private
    authCommunity     log,execute,net   public
    
    disableAuthorization no

## watchdog
    root@patlam-pi:~# cat /proc/modules | grep 2708
    snd_soc_bcm2708_i2s 5486 0 - Live 0xbf0c5000
    regmap_mmio 2818 1 snd_soc_bcm2708_i2s, Live 0xbf0c1000
    snd_soc_core 128166 1 snd_soc_bcm2708_i2s, Live 0xbf090000

    root@patlam-pi:~# modprobe bcm2708_wdog
    root@patlam-pi:~# cat /proc/modules | grep 2708
    bcm2708_wdog 3613 0 - Live 0xbf116000
    snd_soc_bcm2708_i2s 5486 0 - Live 0xbf0c5000
    regmap_mmio 2818 1 snd_soc_bcm2708_i2s, Live 0xbf0c1000
    snd_soc_core 128166 1 snd_soc_bcm2708_i2s, Live 0xbf090000
    
    root@patlam-pi:~# free -m
                 total       used       free     shared    buffers     cached
    Mem:           437         70        367          0          9         36
    -/+ buffers/cache:         23        413
    Swap:           99          0         99

    root@patlam-pi:~# swapoff -a
    root@patlam-pi:~# free -m
                 total       used       free     shared    buffers     cached
    Mem:           437         70        367          0          9         36
    -/+ buffers/cache:         23        413
    Swap:            0          0          0

    root@patlam-pi:~# (: (){ :|:& };:)
    root@patlam-pi:~# w
     00:18:59 up 3 min,  2 users,  load average: 118.69, 25.32, 8.26
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    pi       pts/0    192.168.1.26     00:17   19.00s  2.12s  0.47s sshd: pi [priv]
    pi       pts/1    192.168.1.26     00:18   18.00s  2.15s  0.16s w
    
### /etc/watchdog.conf 
    watchdog-device = /dev/watchdog
    max-load-1              = 24

## その他
### /etc/rc.local  
最下段の行のみを追加  
    # By default this script does nothing.

    # Print the IP address
    _IP=$(hostname -I) || true
    if [ "$_IP" ]; then
      printf "My IP address is %s\n" "$_IP"
    fi

    /opt/aquestalkpi/AquesTalkPi "起動しました、IPアドレス ${_IP}"  | aplay

## アプリケーションのデーモン化  
要 gunicorn

    # cd /prj/patlam-pi
    # sudo gunicorn -D -w 4 -b 0.0.0.0:80 Patlam-pi:app