'''
Testing subscription latency
But there's underlying issue that the code can only measure ssh executition time,
which is not precisely the actual time of subscribing command
'''
from robottelo.common import ssh
from writer import Writer

import sys
import time

old_stdout = sys.stdout
log = open('timing-subscription','w')
# log = open('test.log','w')
sys.stdout = Writer(sys.stdout, log)

'''
for i in range(100):
	print "Attempt: {0}".format(i)
'''

print "Timing register by ak:"
for i in range(20):
    print "Attempt: {0}".format(i)
    result = ssh.command('subscription-manager clean', hostname='10.12.23.223')
    if result.return_code != 0:
       print "Failed to subscribe: {0} and return code: {1}".format(result.stderr,result.return_code)
    start = time.time()
    result = ssh.command('subscription-manager register --activationkey=ak-1 --org="Default_Organization"', hostname='10.12.23.223')
    end = time.time()
    print 'real','	',end-start,'s'

sys.stdout = old_stdout
log.close()
