from robottelo.cli.repository import Repository
from robottelo.cli.repository_set import RepositorySet
print "Disable repositories by groups"
# Group enabling repos
pid = 15
repository_list = [
  [168, 'x86_64', '6Server'],
  [2456,'x86_64', '7Server'],
  [1952,'x86_64', '6.6'],
  [2455,'x86_64', '7.1'],
  [166, 'x86_64', '6Server'],
  [2463,'x86_64', '7Server'],
  [167, 'x86_64', '6Server'],
  [2464,'x86_64', '7Server']
]

for i, repo in enumerate(repository_list):
    repo_id = repo[0]
    basearch = repo[1]
    releasever = repo[2]
    print "Disabling product: {0} with basearch {1} and release {2}".format(repo_id, basearch, releasever)

    # Enable repo from Repository Set
    result = RepositorySet.disable({
      'product-id':pid,
      'basearch':basearch,
      'releasever':releasever,
      'id':repo_id
   })
#repository_list.append([168, 'x86_64', '6Server'])
#repository_list.append([2456,'x86_64','7Server'])
#repository_list.append([])


'''
# Enable repo from Repository Set
result = RepositorySet.enable({
  'product-id':pid,
  'basearch':basearch,
  'releasever':releasever,
  'id':repo_id
})
'''
# verify enabled repository list
result = Repository.list({'organization-id':'1'}, per_page=False)

result.stdout
'''
for repo in repo_list
    print repo['id'],' | ',repo['name']
'''

