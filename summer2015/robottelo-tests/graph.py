import pygal


def generate_bar_chart_stat(stat_dict, head, filename, lengend):
    """Generate Bar chart for stat on concurrent subscription"""
    bar_chart = pygal.Bar()
    bar_chart.title = head
    bar_chart.x_labels = ('min', 'mean', 'max', 'std')
    bar_chart.x_title = 'Statistics'
    bar_chart.y_title = 'Time (s)'
    for key in range(len(stat_dict)):
        bar_chart.add(
            '{0}-{1}'.format(lengend, key),
            stat_dict.get(key)
        )
    bar_chart.render_to_file(filename)


def generate_line_chart_bucketized_stat(stat_dict, head, filename,
                                        bucket_size, num_buckets):
    """Generate Line chart for stat on concurrent subscription"""
    if bucket_size == 0:
        return

    # parameters for formats on charts
    lengend = ('min', 'median', 'max', 'std')
    buckets = [
        '{0}-{1}'.format(
            bucket_size * i + 1,
            bucket_size * (i + 1)
        )
        for i in range(num_buckets)
    ]
    line_chart = pygal.Line()
    line_chart.title = head
    line_chart.x_labels = buckets
    line_chart.x_title = 'Buckets'
    line_chart.y_title = 'Time (s)'
    for stat, stat_value in enumerate(lengend):
        # count min/median/max/std separately
        tmp_list = []
        # accumulate stat item of each client
        for index in range(len(stat_dict)):
            tmp_list.append(stat_dict.get(index)[stat])
        # add list to chart
        line_chart.add(
            lengend[stat],
            tmp_list
        )
    line_chart.render_to_file(filename)


def generate_stacked_line_chart_raw(time_result_dict, head, filename):
    """Generate Stacked-Line chart for raw data of ak/att/del/reg"""
    stackedline_chart = pygal.StackedLine(
        fill=True, show_dots=False, range=(0, 50)
    )
    # compute labels
    max_label = len(time_result_dict.get('thread-0'))
    stackedline_chart.x_labels = map(str, range(1, max_label))
    # set title, x/y-axis title
    stackedline_chart.title = head
    stackedline_chart.x_title = 'Iterations'
    stackedline_chart.y_title = 'Time (s)'
    # for each client, add time list into chart
    for thread in range(len(time_result_dict)):
        key = 'thread-{}'.format(thread)
        time_list = time_result_dict.get(key)
        stackedline_chart.add(
            'client-{}'.format(thread),
            time_list
        )
    # save graph as svg file
    stackedline_chart.render_to_file(filename)


def generate_line_chart_raw(time_result_dict, head, filename):
    """Generate Normal Line chart for raw data of ak/att/del/reg"""
    # declare a Line object
    line_chart = pygal.Line(show_dots=False, range=(0, 50))
    # compute labels
    max_label = len(time_result_dict.get('thread-0'))
    line_chart.x_labels = map(str, range(1, max_label))
    # set title, x/y-axis title
    line_chart.title = head
    line_chart.x_title = 'Iterations'
    line_chart.y_title = 'Time (s)'
    # for each client, add time list into chart
    for thread in range(len(time_result_dict)):
        key = 'thread-{}'.format(thread)
        time_list = time_result_dict.get(key)
        line_chart.add(
            'client-{}'.format(thread),
            time_list
        )
    # save graph as svg file
    line_chart.render_to_file(filename)
