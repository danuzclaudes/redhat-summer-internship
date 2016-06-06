"""Test utilities for writing performance tests

Define ConcurrentTestCase as parent class of writting Subscribe by AK,
Subscribe by register and attach, Subscription Deletion.

"""
import csv

from robottelo.common import conf, ssh
from robottelo.test import TestCase

from robottelo.performance.constants import(
    DEFAULT_ORG,
    NUM_THREADS,
)
from robottelo.performance.graph import (
    generate_line_chart_bucketized_stat,
    generate_stacked_line_chart_raw
)
from robottelo.performance.thread import (
    DeleteThread,
    SubscribeAKThread,
    SubscribeAttachThread
)
from robottelo.performance.stat import generate_stat_for_concurrent_thread


class ConcurrentTestCase(TestCase):
    """Test utilities for writing performance tests.

    Define ConcurrentTestCase as base class of performance test case:

    1. concurrent subscription by AK,
    2. concurrent subscription by register and attach,
    3. concurrent subscription deletion.

    """

    @classmethod
    def setUpClass(cls):
        """Make sure to only read configuration values once."""
        super(ConcurrentTestCase, cls).setUpClass()

        # general running parameters
        cls.num_threads = NUM_THREADS
        cls.num_buckets = conf.properties['performance.csv.num_buckets']
        cls.vm_list = []
        cls.org_id = cls._get_organization_id()  # get organization-id
        cls.sub_id = ''
        cls.num_iterations = 0     # depend on # of threads or clients
        cls.bucket_size = 0        # depend on # of iterations on each thread

        cls._convert_to_numbers()  # read in string type, convert to numbers
        cls._get_vm_list()         # read in list of virtual machines

        # read default organization from constant module
        cls.default_org = DEFAULT_ORG

    @classmethod
    def _convert_to_numbers(cls):
        """read in string type series, convert to numbers"""
        cls.num_threads = [int(x) for x in cls.num_threads.split(',')]
        cls.num_buckets = int(cls.num_buckets)

    @classmethod
    def _get_vm_list(cls):
        """read in a list of virtual machines ip address"""
        vm_list_string = conf.properties[
            'performance.test.virtual_machines_list']
        cls.vm_list = vm_list_string.split(',')

    @classmethod
    def _set_testcase_parameters(cls, savepoint_name,
                                 raw_file_name, stat_file_name):
        # note: set savepoint empty to continue test without restore
        cls.savepoint = conf.properties.get(savepoint_name, '')
        cls.raw_file_name = raw_file_name
        cls.stat_file_name = stat_file_name

    @classmethod
    def _get_organization_id(cls):
        """Get organization id"""
        result = OrgCli.list(per_page=False)
        if result.return_code != 0:
            cls.logger.error('Fail to get organization id.')
            raise RuntimeError('Invalid organization id. Stop!')
        return result.stdout[0]['id']

    def setUp(self):
        self.logger.debug(
            'Running test %s/%s', type(self).__name__, self._testMethodName)

        # Restore database before concurrent subscription/deletion
        self._restore_from_savepoint(self.savepoint)

    def _restore_from_savepoint(self, savepoint):
        """Restore from savepoint"""
        if savepoint == '':
            self.logger.warning('No savepoint while continuing test!')
            return
        self.logger.info('Reset db from /home/backup/{}'.format(savepoint))
        ssh.command('./reset-db.sh /home/backup/{}'.format(savepoint))

    def _get_subscription_id(self):
        """Get subscription id"""
        result = Subscription.list(
            {'organization-id': self.org_id},
            per_page=False
        )

        if result.return_code != 0:
            self.logger.error('Fail to get subscription id!')
            raise RuntimeError('Invalid subscription id. Stop!')
        subscription_id = result.stdout[0]['id']
        subscription_name = result.stdout[0]['name']
        self.logger.info(
            'Subscribed to {0} with subscription id {1}'
            .format(subscription_name, subscription_id)
        )
        return subscription_id, subscription_name

    def _set_num_iterations(self, total_iterations, current_num_threads):
        """Set # of iterations each thread will conduct.

        :param int total_iterations: total # of iterations for a test case
        :param int current_num_threads: number of clients or threads

        Example:

        1. split 5k total_iterations evenly between 10 clients, thus each
           client would conduct 500 iterations concurrently;
        2. split 6k evenly between 6 clients, thus each client would conduct
           1000 iterations concurrently;

        """
        self.num_iterations = total_iterations / current_num_threads

    def _set_bucket_size(self):
        """Set size for each bucket"""
        bucket = self.num_iterations / self.num_buckets

        # check if num_iterations for each client is smaller than 10
        if bucket > 0:
            self.bucket_size = bucket
        else:
            self.bucket_size = 1

    def _join_all_threads(self, thread_list):
        """Wait for all threads to complete"""
        for thread in thread_list:
            thread.join()

    def _write_raw_csv_file(self, raw_file_name, time_result_dict,
                            current_num_threads, test_case_name):
        """Write raw timing ak/del results to csv file"""
        self.logger.debug(
            'Timing result is: {}'.format(time_result_dict))

        with open(raw_file_name, 'a') as handler:
            writer = csv.writer(handler)
            writer.writerow([test_case_name])

            # for each thread, write its head and data
            for i in range(current_num_threads):
                writer.writerow([
                    'client-{}'.format(i)
                ])
                writer.writerow(time_result_dict.get('thread-{}'.format(i)))
            writer.writerow([])

    def _write_raw_att_csv_file(self, raw_file_name, time_result_dict,
                                current_num_threads, test_case_name):
        """Write raw timing att results to csv file"""
        self.logger.debug("Timing result is: {}".format(time_result_dict))
        with open(raw_file_name, 'a') as handler:
            writer = csv.writer(handler)
            writer.writerow([test_case_name])

            # for each thread, write its head and data
            for i in range(current_num_threads):
                writer.writerow(['client-{}'.format(i)])
                for index in range(3):
                    writer.writerow(
                        time_result_dict.get('thread-{}'.format(i))[index])
                    writer.writerow([])

    def _write_stat_csv_file(self, stat_file_name, time_result_dict,
                             current_num_threads, test_case_name, is_attach):
        """Generate statistical result of concurrent ak/del/att"""
        with open(stat_file_name, 'a') as handler:
            writer = csv.writer(handler)
            writer.writerow([test_case_name])

            # 1) write stat-per-client-bucketized result of ak/del/att
            writer.writerow(['stat-per-client-bucketized'])
            self._write_stat_per_client_bucketized(
                stat_file_name,
                time_result_dict,
                current_num_threads,
                is_attach
            )
            writer.writerow([])

            # 2) write stat-per-test-bucketized result of ak/del/att
            writer.writerow(['stat-per-test-bucketized'])
            self._write_stat_per_test_bucketized(
                stat_file_name,
                time_result_dict,
                is_attach)
            writer.writerow([])

            # 3) write stat-per-client result of ak/del/att
            writer.writerow(['stat-per-client'])
            self._write_stat_per_client(
                stat_file_name,
                time_result_dict,
                current_num_threads,
                is_attach)
            writer.writerow([])

            # 4) write stat-per-test result of ak/del/att
            writer.writerow(['stat-per-test'])
            self._write_stat_per_test(
                stat_file_name,
                time_result_dict,
                is_attach)
            writer.writerow([])

    def _write_stat_per_client_bucketized(
            self, stat_file_name,
            time_result_dict,
            current_num_threads,
            is_attach):
        """Write bucketized stat of per-client results to csv file

        note: each bucket is a split of a client i

        """
        for i in range(current_num_threads):
            if is_attach:
                time_list = time_result_dict.get('thread-{}'.format(i))[2]
            else:
                time_list = time_result_dict.get('thread-{}'.format(i))
            thread_name = 'client-{}'.format(i)
            stat_dict = generate_stat_for_concurrent_thread(
                thread_name,
                time_list,
                stat_file_name,
                self.bucket_size,
                self.num_buckets
            )

            generate_line_chart_bucketized_stat(
                stat_dict,
                'Concurrent Subscription Stat - per client bucketized '
                'client-{0} total-{1}-clients'.format(i, current_num_threads),
                'stat-client-{0}-bucketized-{1}-clients.svg'
                .format(i, current_num_threads),
                self.bucket_size,
                self.num_buckets
            )

    def _write_stat_per_test_bucketized(
            self, stat_file_name,
            time_result_dict,
            is_attach):
        """Write bucketized stat of per-test to csv file

        note: each bucket of all clients would merge into a chunk;
        generate stat for each such chunk. For example::

            Input: # of clients = 10
            thread-0: [(50 data) | (50 data)|...]
            thread-1: [(50 data) | (50 data)|...]
            ...
            thread-9: [(50 data) | (50 data)|...]
            Output:
            sublist [500 data in all first buckets of each thread]
                    [500]...[500]

        """
        # parameters for generating bucketized line chart
        stat_dict = {}
        return_stat = {}
        num_clients = len(time_result_dict)

        for i in range(self.num_buckets):
            chunks_bucket_i = []
            for j in range(len(time_result_dict)):
                if is_attach:
                    time_list = time_result_dict.get('thread-{}'.format(j))[2]
                else:
                    time_list = time_result_dict.get('thread-{}'.format(j))
                # slice out bucket-size from each client's result and merge
                chunks_bucket_i += time_list[
                    i * self.bucket_size: (i + 1) * self.bucket_size
                ]

            # for each chunk i, compute and output its stat
            return_stat = generate_stat_for_concurrent_thread(
                'bucket-{}'.format(i),
                chunks_bucket_i,
                stat_file_name,
                len(chunks_bucket_i), 1)

            # for each chunk i, add stat into final return_dict
            stat_dict.update({
                i: return_stat.get(0, (0, 0, 0, 0))
            })

        # create graph based on stats of all chunks
        generate_bar_chart_stat(
            stat_dict,
            'Concurrent Subscription Stat - per test bucketized '
            '({} clients)'.format(num_clients),
            'stat-test-bucketized-{}-clients.svg'.format(num_clients),
            self.bucket_size,
            self.num_buckets
        )

    def _write_stat_per_client(self, stat_file_name, time_result_dict,
                               current_num_threads, is_attach):
        """Write stat of per-client results to csv file

        note: take the full list of a client i; calculate stat on the list

        """
        stat_dict = {}
        return_stat = {}
        num_clients = len(time_result_dict)
        for i in range(current_num_threads):
            if is_attach:
                time_list = time_result_dict.get('thread-{}'.format(i))[2]
            else:
                time_list = time_result_dict.get('thread-{}'.format(i))
            thread_name = 'client-{}'.format(i)

            # for each client i, compute and output its stat
            return_stat = generate_stat_for_concurrent_thread(
                thread_name,
                time_list,
                stat_file_name,
                len(time_list), 1)

            # for each chunk i, add stat into final return_dict
            stat_dict.update({
                i: return_stat.get(0, (0, 0, 0, 0))
            })

        # create graph based on stats of all clients
        generate_bar_chart_stat(
            stat_dict,
            'Concurrent Subscription Stat - per client '
            '({} clients)'.format(num_clients),
            'stat-per-client-{}-clients.svg'.format(num_clients),
            'client'
        )

    def _write_stat_per_test(self, stat_file_name,
                             time_result_dict, is_attach):
        """Write stat of per-test results to csv file

        note: take the full dictionary of test and calculate overall stat

        """
        full_list = []  # list containing 1st to 5kth data point
        num_clients = len(time_result_dict)

        for i in range(len(time_result_dict)):
            if is_attach:
                time_list = time_result_dict.get('thread-{}'.format(i))[2]
            else:
                time_list = time_result_dict.get('thread-{}'.format(i))
            full_list += time_list

        stat_dict = generate_stat_for_concurrent_thread(
            'test-{}'.format(len(time_result_dict)),
            full_list,
            stat_file_name,
            len(full_list), 1)

        generate_bar_chart_stat(
            stat_dict,
            'Concurrent Subscription Stat - per test '
            '({} clients)'.format(num_clients),
            'stat-per-test-{}-clients.svg'.format(num_clients),
            'test'
        )

    def kick_off_ak_test(self, current_num_threads, total_iterations):
        """Refactor out concurrent register by ak test case

        :param int current_num_threads: number of threads
        :param int total_iterations: # of iterations a test case would run

        """
        # check if number of threads are mapped with number of vms
        current_vm_list = self.vm_list[:current_num_threads]
        self.assertEqual(len(current_vm_list), current_num_threads)

        # Parameter for statistics files
        self._set_num_iterations(total_iterations, current_num_threads)
        self._set_bucket_size()

        # Create a list to store all threads
        thread_list = []
        # Create a dictionary to store all timing results from each client
        time_result_dict = {}

        # Create new threads and start each thread mapped with a vm
        for i in range(current_num_threads):
            thread_name = 'thread-{}'.format(i)
            time_result_dict[thread_name] = []
            thread = SubscribeAKThread(
                i, thread_name, time_result_dict,
                self.num_iterations, self.ak_name,
                self.default_org, current_vm_list[i])
            thread.start()
            thread_list.append(thread)

        # wait all threads in thread list
        self._join_all_threads(thread_list)

        # write raw result of ak
        self._write_raw_csv_file(
            self.raw_file_name,
            time_result_dict,
            current_num_threads,
            'raw-ak-{}-clients'.format(current_num_threads))

        # write stat result of ak
        self._write_stat_csv_file(
            self.stat_file_name,
            time_result_dict,
            current_num_threads,
            'stat-ak-{}-clients'.format(current_num_threads), False)

    def kick_off_att_test(self, current_num_threads, total_iterations):
        """Refactor out concurrent register and attach test case

        :param int current_num_threads: number of threads
        :param int total_iterations: # of deletions a test case would run

        """
        # check if number of threads are mapped with number of vms
        current_vm_list = self.vm_list[:current_num_threads]
        self.assertEqual(len(current_vm_list), current_num_threads)

        # Parameter for statistics files
        self._set_num_iterations(total_iterations, current_num_threads)
        self._set_bucket_size()

        # Create a list to store all threads
        thread_list = []
        # Create a dictionary to store all timing results from each client
        time_result_dict = {}

        # Create new threads and start each thread mapped with a vm
        for i in range(current_num_threads):
            thread_name = 'thread-{}'.format(i)
            time_result_dict[thread_name] = [[], [], []]

            thread = SubscribeAttachThread(
                i, thread_name, time_result_dict,
                self.num_iterations, self.sub_id,
                self.default_org, self.environment,
                current_vm_list[i])
            thread.start()
            thread_list.append(thread)

        # wait all threads in thread list
        self._join_all_threads(thread_list)

        # write raw result of att
        self._write_raw_att_csv_file(
            self.raw_file_name,
            time_result_dict,
            current_num_threads,
            'raw-att-{}-clients'.format(current_num_threads))

        # write stat result of att
        self._write_stat_csv_file(
            self.stat_file_name,
            time_result_dict,
            current_num_threads,
            'stat-att-{}-clients'.format(current_num_threads), True)

    def kick_off_del_test(self, current_num_threads):
        """Refactor out concurrent system deletion test case

        :param int current_num_threads: number of threads
        :param int total_iterations: FIXME

        """
        # Get list of all uuids of registered systems

        self.logger.info('Retrieve list of uuids of all registered systems:')
        uuid_list = self._get_registered_uuids()

        # Parameter for statistics files
        total_iterations = len(uuid_list)

        self._set_num_iterations(total_iterations, current_num_threads)
        self._set_bucket_size()

        # Create a list to store all threads
        thread_list = []
        # Create a dictionary to store all timing results from each thread
        time_result_dict = {}

        # Create new threads and start the thread which has sublist of uuids
        for i in range(current_num_threads):
            time_result_dict['thread-{}'.format(i)] = []
            thread = DeleteThread(
                i, 'thread-{}'.format(i),
                uuid_list[
                    self.num_iterations * i:
                    self.num_iterations * (i + 1)
                ],
                time_result_dict
            )
            thread.start()
            thread_list.append(thread)

        # wait all threads in thread list
        self._join_all_threads(thread_list)

        # write raw result of del
        self._write_raw_csv_file(
            self.raw_file_name,
            time_result_dict,
            current_num_threads,
            'raw-del-{}-clients'.format(current_num_threads))

        # write stat result of del
        self._write_stat_csv_file(
            self.stat_file_name,
            time_result_dict,
            current_num_threads,
            'stat-del-{}-clients'.format(current_num_threads), False)
