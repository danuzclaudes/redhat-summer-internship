import pygal

def generate_stacked_line_chart_raw(time_result_dict, head, filename):
    """Generate Stacked-Line chart for subscription by attach and ak"""
    stackedline_chart = pygal.StackedLine(fill=True, show_dots=False, range=(0, 50))
    stackedline_chart.x_labels = map(str, range(1, 2500))
    # set title with subtitle
    stackedline_chart.title = head
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
    """Generate Normal Line chart for subscription by attach and ak"""
    line_chart = pygal.Line(show_dots=False, range=(0, 50))
    line_chart.x_labels = map(str, range(1, 2500))
    # set title with subtitle
    stackedline_chart.title = head
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

test_category = 'raw-activationKey'
current_num_threads = 2
head = 'Concurrent Subscription Raw - '\
'({0}-{1}-clients)'.format(test_category, current_num_threads)
filename = '{0}-{1}-clients-stacked-line.svg'.format(test_category, current_num_threads)

generate_stacked_line_chart_raw(
    time_result_dict, head, filename
)

test_category = 'raw-activationKey'
current_num_threads = 2
head = 'Concurrent Subscription Raw - '\
'({0}-{1}-clients)'.format(test_category, current_num_threads)
filename = '{0}-{1}-clients-line.svg'.format(test_category, current_num_threads)

generate_line_chart_raw(
    time_result_dict, head, filename
)

"""
time_result_dict = {'thread-9': [[53.52, 17.1, 15.72, 12.78, 13.93, 11.59, 11.93, 11.53, 11.06, 12.31], [55.56, 22.98, 19.89, 15.97, 18.42, 21.54, 19.05, 19.61, 21.95, 15.55], [109.08000000000001, 40.08, 35.61, 28.75, 32.35, 33.129999999999995, 30.98, 31.14, 33.01, 27.86]], 'thread-8': [[66.83, 22.46, 12.5, 12.22, 10.88, 14.36, 12.17, 13.46, 15.25, 10.36], [55.95, 24.97, 17.18, 19.16, 19.93, 17.84, 18.21, 18.75, 17.05, 17.69], [122.78, 47.43, 29.68, 31.380000000000003, 30.810000000000002, 32.2, 30.380000000000003, 32.21, 32.3, 28.05]], 'thread-7': [[66.75, 14.8, 13.01, 12.59, 11.68, 12.93, 13.06, 12.64, 11.41, 12.21], [42.32, 19.66, 13.67, 16.97, 21.62, 18.37, 16.75, 20.63, 20.53, 16.69], [109.07, 34.46, 26.68, 29.56, 33.3, 31.3, 29.810000000000002, 33.269999999999996, 31.94, 28.900000000000002]], 'thread-6': [[57.03, 20.2, 13.96, 13.73, 11.08, 12.56, 10.25, 12.54, 11.61, 10.79], [52.43, 29.16, 22.88, 15.82, 18.99, 20.32, 20.72, 21.12, 17.07, 18.88], [109.46000000000001, 49.36, 36.84, 29.55, 30.07, 32.88, 30.97, 33.66, 28.68, 29.669999999999998]], 'thread-5': [[66.49, 17.51, 17.3, 15.02, 11.93, 13.31, 12.56, 10.16, 13.67, 10.78], [42.96, 26.59, 14.81, 18.06, 17.84, 18.37, 20.39, 21.88, 17.04, 17.81], [109.44999999999999, 44.1, 32.11, 33.08, 29.77, 31.68, 32.95, 32.04, 30.71, 28.589999999999996]], 'thread-4': [[66.66, 16.4, 11.41, 12.37, 14.06, 11.36, 10.71, 11.64, 10.49, 13.83], [42.99, 19.29, 14.21, 21.73, 16.58, 20.03, 21.42, 19.99, 21.45, 20.28], [109.65, 35.69, 25.62, 34.1, 30.64, 31.39, 32.13, 31.63, 31.939999999999998, 34.11]], 'thread-3': [[66.62, 16.17, 13.61, 14.85, 12.97, 12.25, 12.64, 13.66, 12.57, 11.95], [43.98, 31.63, 15.57, 19.44, 17.55, 18.12, 20.6, 18.3, 17.52, 17.96], [110.6, 47.8, 29.18, 34.29, 30.520000000000003, 30.37, 33.24, 31.96, 30.09, 29.91]], 'thread-2': [[66.97, 16.49, 13.02, 11.88, 12.01, 11.51, 10.11, 12.27, 11.99, 12.67], [42.18, 19.7, 14.83, 23.61, 17.89, 20.53, 22.66, 18.55, 17.55, 16.37], [109.15, 36.19, 27.85, 35.49, 29.9, 32.04, 32.769999999999996, 30.82, 29.54, 29.04]], 'thread-1': [[67.45, 16.87, 12.52, 11.99, 12.81, 11.81, 10.63, 11.09, 11.67, 11.63], [44.91, 31.11, 25.39, 15.85, 19.58, 21.74, 19.7, 20.77, 18.68, 17.69], [112.36, 47.980000000000004, 37.91, 27.84, 32.39, 33.55, 30.33, 31.86, 30.35, 29.32]], 'thread-0': [[53.8, 17.25, 13.42, 14.65, 12.03, 12.28, 15.74, 12.73, 12.12, 14.46], [55.52, 20.4, 21.87, 13.95, 18.96, 19.54, 16.71, 18.06, 20.3, 16.08], [109.32, 37.65, 35.29, 28.6, 30.990000000000002, 31.82, 32.45, 30.79, 32.42, 30.54]]}
"""
