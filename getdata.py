#!/usr/bin/env python3
import getpass
import os

from boaapi.boa_client import BoaClient
from boaapi.status import CompilerStatus, ExecutionStatus

client = None
def getclient():
    client = BoaClient()
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()
    client.login(user, getpass.getpass())
    print('successfully logged in to Boa API')
    return client

def getoutput(id, filename=None):
    global client

    if not filename:
        filename = f'data/txt/boa-job{id}-output.txt'
    else:
        filename = f'data/txt/{filename}'

    if os.path.exists(filename):
        return

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/txt'):
        os.mkdir('data/txt')

    if not client:
        client = getclient()

    job = client.get_job(id)

    if job.is_running():
        print(f'waiting on {job.id}')

    if job.wait():
        print(f'downloading {job.id} to {filename}')
        with open(filename, 'w') as f:
            f.write(job.output())
    elif job.compiler_status is CompilerStatus.ERROR:
        print(f'job {job.id} had compile error')
    elif job.exec_status is ExecutionStatus.ERROR:
        print(f'job job.id had exec error')

getoutput(97667, filename='counts.txt')

getoutput(97666, filename='hashes.txt')

getoutput(96389, filename='rq1.output.txt')
getoutput(96238, filename='rq2.output.txt')
getoutput(96390, filename='rq4.output.txt')

if client:
    client.close()
    print('client closed')
