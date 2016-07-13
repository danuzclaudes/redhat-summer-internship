# Issue: https://pulp.plan.io/issues/1684
# https://pulp.plan.io/issues/1406
# http://yum.baseurl.org/wiki/RepoCreate


ls -al /etc/yum.repos.d/
pulp-admin rpm repo create --repo-id repo1 --feed \
  http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/zoo/
pulp-admin rpm repo sync run --repo-id repo1
pulp-admin rpm repo content rpm --repo-id repo1 \
  --str-eq "name=mouse"


# Create a repo and publish with Pulp
pulp-admin rpm repo create --repo-id repo1 --feed \
  https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/
pulp-admin rpm repo sync run --repo-id=repo1

# Yum update on client aimed at the repo
sudo yum --disablerepo="*" --enablerepo="*pulp*" update

# Remove a specific RPM for testing purpose
pulp-admin rpm repo remove rpm --repo-id repo1 --match "name=mouse"
pulp-admin rpm repo content rpm --repo-id repo1 \
  --str-eq "name=mouse"
# Add a newer RPM to the repo in pulp and re-publish
pulp-admin rpm repo uploads rpm --repo-id repo1 \
  --file ./mouse-0.1.12-1.noarch.rpm
pulp-admin rpm repo content rpm --repo-id repo1 \
  --str-eq "name=mouse"
pulp-admin rpm repo sync run --repo-id=repo1

# Yum update on the client again, and yum breaks? how exactly?
sudo yum --disablerepo="*" --enablerepo="*pulp*" update


# Software Regression
# A regression is where we broke something by fixing something else.
# An idea for any software repository.
# For example, consider that firefox is available in a Fedora repo.
# A bug fix release comes out that's newer, so that gets added to the same repo.
# There's no need to remove the older one. In fact some people may prefer to keep having the old one available in case the new one has a regression.

# When a regression is found, the best way to resolve it is to find the regression range (by doing a binary search using a testcase and nightly builds) and then the checkin that caused the regression. The bug reporting the regression is then set to block the bug that caused the regression. Using the example above, if bug 100 resulted in the functional regression reported in bug 200, then bug 200 would be marked as blocking bug 100.





# upstream -> local/pulp server (cache server), do an `yum update`, will sync from upstream





# Create repo, copy stuff into it, then publish it.
# create and sync are good.
# find an RPM that has two different versions in the repo.
# create a new repo, and copy the older of the rpm version into it.
# Setup that repo on a host, and install the package.
# copy a newer version into the repo and re-publish
# yum update on the client, and see what happens


# find an RPM that has two different versions in the repo.
pulp-admin rpm repo create --repo-id repo1 --feed \
  https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/
pulp-admin rpm repo sync run --repo-id=repo1
pulp-admin rpm repo content rpm --repo-id repo1 \
  --str-eq "name=walrus"

# create a new repo, and copy the older of the rpm version into it.
pulp-admin rpm repo create --repo-id repo2
pulp-admin rpm repo content rpm --repo-id repo1 \
  --str-eq="version=0.71"
pulp-admin rpm repo copy rpm --from-repo-id repo1 \
  --to-repo-id repo2 --str-eq="version=0.71"
pulp-admin rpm repo content rpm --repo-id repo2

# Setup that repo on a host, and install the package.
# pulp-admin rpm repo export run --repo-id repo2 --export-dir "/home/vagrant/devel/pulp-dev/repo2"
# pulp-admin rpm repo update --repo-id repo2 --feed "/home/vagrant/devel/pulp-dev/repo2"
# pulp-admin rpm repo publish status --repo-id repo2
pulp-admin rpm repo publish run --repo-id repo2
phttp https://dev/pulp/repos/repo2  # check if error occurs

# copy a newer version into the repo and re-publish
pulp-admin rpm repo copy rpm --from-repo-id repo1 \
  --to-repo-id repo2 --str-eq="version=5.21"
pulp-admin rpm repo content rpm --repo-id repo2
pulp-admin rpm repo publish run --repo-id repo2
phttp https://dev/pulp/repos/repo2  # check if error occurs

# yum update on the client, and see what happens???
sudo yum --disablerepo="*" --enablerepo="*pulp*" update


# You want to have your pulp server with a published repo, and a machine that is setup to use that repo.
# Then *somehow* you need to get two rpms with the same names and different versions into pulp. Sync of that zoo repo is a reasonable way.
# You want the older rpm in the repo by itself, then install it on the host.
# Then add the newer rpm to the repo, and run "yum update" on the host.
# And see what happens. Probably it will just update fine.




