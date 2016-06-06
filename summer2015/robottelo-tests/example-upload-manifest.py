# Testing upload manifest to Red Hat Satellite 6 by Robottelo Framework
import os
import sys
import time

os.getcwd()
#sys.stdout = open('timing-upload','w')
#os.chdir('/home/chozhang/Documents/robottelo/robottelo/')

from robottelo.common import ssh
from robottelo.cli.subscription import Subscription

# open log file
print 'Timing uploading manfest to server:'
r = ssh.command('hostname')
print r.stdout[0]
ssh.command('rm test_manifest.zip')

ssh.upload_file('/home/chozhang/Documents/satellite6/20150526-10k-RHEL-Manifest.zip','test_manifest.zip')
start = time.time()
result = Subscription.upload({
  'file':'./test_manifest.zip',
  'organization-id':'1'
})

if result.return_code != 0:
  print "Failed to upload manifest: {0} and return code: {1}" \
	.format(result.stderr, result.return_code)
else:
   # print subscription list
   result = Subscription.list({'organization-id':'1'}, per_page=False)
   if result.return_code == 0:
      print "Subscription name: ",result.stdout[0]['name']
      print "Subscription id: ",result.stdout[0]['id'] 
      print "Upload successful!"
   else:
      print "Failed to list subscriptions: {0} and return code: {1}".format(result.stderr, result.return_code)
     

end = time.time()
print 'real','   ',end-start,'s'

from robottelo.cli.org import Org
# update organization id
Org.update({'id':'1', 'redhat-repository-url':'http://172.16.20.12/pub'})
result = Org.info({'id':'1'})
if result.return_code == 0:
   print "Organization CDN URL: ",result.stdout['red-hat-repository-url']
