from robottelo.performance.graph import generate_line_chart_bucketized_stat
from robottelo.performance.stat import generate_stat_for_concurrent_thread
def write_stat_per_test_bucketized(
    time_result_dict, is_attach=True):
    stat_dict = {}
    return_stat = {}
    num_clients = len(time_result_dict)
    for i in range(10):
        chunks_bucket_i = []
        for j in range(len(time_result_dict)):
            if is_attach:
                time_list = time_result_dict.get('thread-{}'.format(j))[2]
            else:
                time_list = time_result_dict.get('thread-{}'.format(j))
            # slice out bucket-size from each client's result and merge
            chunks_bucket_i += time_list[
                i * 125: (i + 1) * 125
            ]
        # for each chunk i, compute and output its stat
        return_stat = generate_stat_for_concurrent_thread(
            'bucket-{}'.format(i),
            chunks_bucket_i,
            'csv-test-per-client.csv',
            len(chunks_bucket_i), 1)
        # for each chunk i, add stat into final return_dict
        stat_dict.update({
            i: return_stat.get(0, (0, 0, 0, 0))
        })
    # create graph based on stats of all chunks
    generate_line_chart_bucketized_stat(
        stat_dict,
        'Concurrent Subscription Stat - per test bucketized '
        '({} clients)'.format(num_clients),
        'stat-test-bucketized-{}-clients.svg'.format(num_clients),
        500,
        10
    )

write_stat_per_test_bucketized(
    time_result_dict,
)
