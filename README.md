# Linuxへの変更点

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

### /etc/default/snmpd  
    $ diff snmpd snmpd.org
    16c16
    < TRAPDRUN=yes
    ---
    > TRAPDRUN=no

### /etc/rc.local  
最下段の行のみを追加  
    # By default this script does nothing.

    # Print the IP address
    _IP=$(hostname -I) || true
    if [ "$_IP" ]; then
      printf "My IP address is %s\n" "$_IP"
    fi

    /opt/aquestalkpi/AquesTalkPi "起動しました、IPアドレス ${_IP}"  | aplay

# アプリケーションのデーモン化  
要 gunicorn

    # cd /prj/patlam-pi
    # sudo gunicorn -D -w 4 -b 0.0.0.0:80 Patlam-pi:app