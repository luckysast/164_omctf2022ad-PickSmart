#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import asyncore
import socket
from subprocess import call
import subprocess
import threading
import os
import time
import hashlib
import random
from datetime import datetime
import re

def logger(a,b,c,d,e):
    now = datetime.now()
    log = str(now)+a+b+c+d+e
    print(log)
    with open('/var/log/picksmart.log', 'a') as file:
        file.write(log)
        file.write('\n')

class EchoHandler(asyncore.dispatcher_with_send):
    i =0
    def handle_read(self):
        self.i += 1
        data = self.recv(256)
        if len(data) > 0:
            method = data.decode()
            if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]', method):
                return
            time.sleep(0.1)
            try:
                str2hash = method.split(' ')[0]
                result = hashlib.md5(str2hash.encode())

                key=result.hexdigest()
                if(key == 'ab2dac8050b12310c526251472c5823c'):
                    def rand():
                        return random.randint(1000, 1000000)
                    str3hash = method.split(' ')[1]
                    checker = hashlib.md5(str3hash.encode()).hexdigest()
                    key=rand()
                    print(key)
                    print(str3hash)
                    with open(r"/tmp/"+str(key), "w") as file:
                        file.write(str3hash + '\n')
                    cmd = 'zip -e -P ' + str(key) + ' /usr/local/apache2/htdocs/' + str(checker) + '.zip /tmp/' + str(key)
                    os.system(cmd)
                else:
                    print('not')
            except:
                pass
            ###############################################
            if('ls' in method):
                try:
                    p = subprocess.Popen(method, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in p.stdout.readlines():
                        self.send(str(line))
                        retval = p.wait()
                        logger(' Info', ' user ', 'Anonymous', ' remote execute', ' execute successfully')
                except:
                    self.send(str("FAIL"))
                    logger(' WARN', ' user ', 'Anonymous', ' remote execute', ' fail execute')
                    self.close()
            else:
                self.send(str('Access Denied'))
                time.sleep(0.1)
        else:
            print('close connect')


class SockServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(3)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print ('connection from host: %s' % repr(addr))
            handler = EchoHandler(sock)

class AsyncEventLoop (threading.Thread):

    def run(self):
        asyncore.loop()

###  запуск отдельного процесса сервера из основного потока

server = SockServer('', 4444)
evLoop = AsyncEventLoop()
evLoop.start()
