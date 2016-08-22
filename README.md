# redhat-summer-internship
This is the coding playground during the internship. Many thanks to my mentors,
my teammates and all who have helped me to learn!

## Portal to commits and code-reviews in summer 2015
For all the merged pull requests
contributed to [Robottelo](https://github.com/SatelliteQE/robottelo) in summer 2015,
please look [here](https://github.com/SatelliteQE/robottelo/commits?author=danuzclaudes).

## Portal to commits and code-reviews in summer 2016
For all Jenkins Job Builder scripts in YAMLs, please look
[here](https://github.com/pulp/pulp_packaging/pulls?q=is%3Apr+author%3Adanuzclaudes).

For all the merged pull requests
contributed to [Pulp Smash](https://github.com/PulpQE/pulp-smash) in summer 2016, please
look
[here](https://github.com/PulpQE/pulp-smash/pulls?q=danuzclaudes).

For all blog posts published on Pulp's official blog site, please look
[here](http://www.pulpproject.org/tag/pulpqe-intern/).


## About the internship in summer 2015 My main job for the 2015's internship was to
characterize the performance of *Red Hat Satellite*, which is an **open-source**
life-cycle management system. It can ​register and subscribe​ **physical,
virtual or cloud** servers, and ​can synchronize​ them with the Red Hat CDN in
order to deploy and manage softwares and services in large scale. *Robottelo* is an
automated test suite for Satellite's Command Line Interface (CLI) and RESTful API tests.


## What I have achieved in summer 2015
- Automation
  * I automated​ the operations of register, subscription and synchronization for
    performance-testing purpose. They were ​scale​d up by running more than
5,000 times. ​The​ average time latency as well as other system metrics were
measured. But I not only run them sequentially; I also run them
​**concurrently**​. So for example, I could register 2 servers at same time,
register 4 at same time, and 6, 8, 10 using multi-threaded programming and virtual
machines. This is how I scaled up these operations.
- Analytics
  * I extracted these performance data, ​analyze​ and ​**visualize**​
    them using Python libraries. Thus I could know how will the performance drop when the
operations have scaled; will the running time grow linearly or even exponentially? All
these processes, from bare­-metal Linux servers to performance tests, from statistical
computation to visualization, were automated and can be executed within just one click of
command line​.
- Coding and Teamwork
  * All of these code were submitted for **code reviews** thru pull requests, and they are
    successfully [merged into Robottelo's master
branch](https://github.com/SatelliteQE/robottelo/pulls?q=iauthor%3Adanuzclaudes).
Therefore, I've established the new performance module into this framework.
  * I've also joined daily **scrum meetings**, and **continuous integration (CI)**
    sessions. I really learned a lot thru the discussions, designs, reviews, reporting and
presentations. Thanks very much to all who were nice and helpful!


## About the internship in summer 2016
## What I have achieved in summer 2016
