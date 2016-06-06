from robottelo.common import ssh
from robottelo.cli.subscription import Subscription

org_id=1
time_list = []

result=Subscription.list({'organization-id':org_id},per_page=False)
if result.return_code == 0:
   print "Successful"
   print result.stderr
   print result.stderr.split()[1]

   

   #print result.stderr.split(" ")[2].split("elapsed")
   #time_list.append(result.stderr.split(" ")[2].split("elapsed")[0])

