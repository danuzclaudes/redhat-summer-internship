from robottelo.performance.graph import generate_bar_chart_stat
from robottelo.performance.stat import generate_stat_for_concurrent_thread
def write_stat_per_test(time_result_dict, is_attach=True):
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
        'csv-test-per-client.csv',
        len(full_list), 1)
    generate_bar_chart_stat(
        stat_dict,
        'Concurrent Subscription Stat - per test '
        '({} clients)'.format(num_clients),
        'stat-per-test-{}-clients.svg'.format(num_clients),
        'test'
    )

write_stat_per_test(time_result_dict)
