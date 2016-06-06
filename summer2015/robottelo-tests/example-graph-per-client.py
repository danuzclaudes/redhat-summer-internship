from robottelo.performance.graph import generate_bar_chart_stat
from robottelo.performance.stat import generate_stat_for_concurrent_thread
def write_stat_per_client(time_result_dict,
                          current_num_threads, is_attach=True):
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
            'csv-test-per-client.csv',
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

write_stat_per_client(time_result_dict, 4)
