cd /etc/zabbix/zabbix_agent2.d/plugins.d
wget https://raw.githubusercontent.com/YL20181120/supervisor_zabbix/main/supervisor.conf
cd /etc/zabbix/
mkdir scripts
cd scripts/
wget https://raw.githubusercontent.com/YL20181120/supervisor_zabbix/main/script/supervisor.py
chmod a+x supervisor.py 
systemctl restart zabbix-agent2


cd /etc/zabbix/zabbix_agent2.d/plugins.d
rm -f ssl_expire_check.conf
wget https://raw.githubusercontent.com/YL20181120/supervisor_zabbix/main/ssl_expire_check.conf
cd /etc/zabbix/scripts
rm -f ssl_expire_check.py
wget https://raw.githubusercontent.com/YL20181120/supervisor_zabbix/main/script/ssl_expire_check.py
chmod a+x ssl_expire_check.py
systemctl restart zabbix-agent2