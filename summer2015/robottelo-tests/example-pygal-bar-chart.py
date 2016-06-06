import pygal
from robottelo.performance.graph import generate_bar_chart_stat
dict={}
dict.update({0:(11.289999999999999,13.803439999999998,27.369999999999997,1.9751443912787743)})
dict.update({1:(11.49,13.2872,19.109999999999999,1.3601191712493432)})
dict.update({2:(11.17,13.058319999999998,17.5,1.1831975226478457)})
dict.update({3:(10.969999999999999,13.069439999999998,18.049999999999997,1.3083169670993342)})
dict.update({4:(11.09,13.000640000000001,17.130000000000003,1.1555270617341682)})
dict.update({5:(10.66,13.040319999999998,16.600000000000001,1.0826056981191261)})
dict.update({6:(11.02,13.107199999999999,18.359999999999999,1.3397036090120829)})
dict.update({7:(10.449999999999999,13.0396,17.75,1.2550737986269969)})
dict.update({8:(11.280000000000001,12.8904,18.02,1.0994197742445786)})
dict.update({9:(11.07,13.401359999999999,17.399999999999999,1.5245218759991608)})

bar_chart = pygal.Bar()
bar_chart.title = 'Stat of Concurrent Tests - per client bucketized'
bar_chart.x_labels = map(str, range(0, 10))
for key in range(len(dict)):
    bar_chart.add('bucket-{}'.format(key), dict.get(key))
bar_chart.render_to_file('example-bar-chart.svg')

head = 'Stat of Concurrent Tests - per client bucketized'
filename = 'example-bar-chart2.svg'
generate_bar_chart_stat(dict, head, filename)
