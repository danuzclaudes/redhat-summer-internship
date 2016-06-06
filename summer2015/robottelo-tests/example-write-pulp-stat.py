import csv
import pygal
from robottelo.performance.stat import generate_stat_for_pulp_sync

total_max_timing={8: [163.91, 160.25, 162.56], 2: [44.49, 47.08, 44.27], 4: [66.82, 66.82, 66.57], 7: [162.62, 155.11, 150.72], 3: [53.76, 54.15, 56.83], 6: [142.15, 134.13, 143.65], 9: [176.56, 173.56, 181.73], 5: [168.62, 113.09, 109.74], 10: [220.67, 195.31, 192.43]}
stat_file_name = 'perf-statistics-sync.csv'
raw_file_name = 'test.svg'

def _write_stat_csv_chart_pulp(total_max_timing):
    """Compute statistics on sync data across tests"""
    with open(stat_file_name, 'w') as handler:
        writer = csv.writer(handler)
        writer.writerow(['concurrent-sync-stat'])
        writer.writerow(['test-case', 'min', 'median', 'max', 'std'])
    stat_dict = {}
    for test in range(2, len(total_max_timing) + 2):
        time_list = total_max_timing.get(test)
        stat_tuple = generate_stat_for_pulp_sync(
            test,
            total_max_timing.get(test),
            stat_file_name,
        )
        # insert each returned tuple of statistics into stat_dict
        stat_dict.update({test: stat_tuple})
    print stat_dict
    generate_pulp_line_chart(
        stat_dict,
        'Satellite 6 Concurrent Syncs',
        raw_file_name,
    )

def generate_pulp_line_chart(stat_dict, head, filename):
    line_chart = pygal.Line()
    line_chart.title = head
    line_chart.x_labels = ['{}'.format(x) for x in range(2, 11)]
    line_chart.x_title = '# of Repos Concurrently Synced'
    line_chart.y_title = 'Time (s)'
    lengend = ('min', 'median', 'max', 'std')
    for count, stat in enumerate(lengend):
        tmp_list = []
        for key, valuelist in stat_dict.iteritems():
            tmp_list.append(valuelist[count])
        print tmp_list
        line_chart.add(stat, tmp_list)
    line_chart.render_to_file(filename)

_write_stat_csv_chart_pulp(total_max_timing) 
