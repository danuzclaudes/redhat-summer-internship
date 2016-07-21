# https://docs.pulpproject.org/plugins/pulp_rpm/user-guide/recipes.html#package-environments
pulp-admin rpm repo create --repo-id repo1 --feed \
    https://repos.fedorapeople.org/repos/pulp/pulp/fixtures/rpm/

pulp-admin rpm repo sync run --repo-id repo1

pulp-admin rpm repo uploads environment --repo-id repo1 \
    --environment-id env1 --name "testing" \
    --description "my testing env"
pulp-admin rpm repo content environment --repo-id repo1

pulp-admin rpm repo delete --repo-id repo1
