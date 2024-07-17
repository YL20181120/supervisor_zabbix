#!/usr/bin/python3

# check_ssl_cert.py - python get info for expired SSL cert
# Copyright 2022 Sharuzzaman Ahmat Raslan <sharuzzaman@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License along with this program. If not, see https://www.gnu.org/licenses/.

from cryptography import x509
import socket
import ssl
import sys
import datetime
import json
import argparse

# create default context
context = ssl.create_default_context()

# override context so that it can get expired cert
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ZABBIX_DISCOVERY = '{#SSL_EXPIRE_HOST}'


def get_expire_days(hostname):
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            data = ssock.getpeercert(True)
            pem_data = ssl.DER_cert_to_PEM_cert(data)
            cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))
            delta = cert_data.not_valid_after - datetime.datetime.utcnow()
            return delta.days


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Supervisor monitoring')
    parser.add_argument('cmd', type=str)
    parser.add_argument('hosts', type=str)
    args = parser.parse_args()

    if args.cmd == 'discovery':
        zabbix_discovery = []
        for host in args.hosts.split(','):
            zabbix_discovery.append({ZABBIX_DISCOVERY: host})
        print(json.dumps(zabbix_discovery))
    elif args.cmd == 'status':
        hosts = args.hosts.split(',')
        data = []
        for host in hosts:
            data.append({host: get_expire_days(host)})
        print(json.dumps(data))
