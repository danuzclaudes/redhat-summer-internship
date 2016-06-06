#!/usr/bin/python
"""python join two lists"""
listone = [1,2,3]
listtwo = [4,5,6]
# print listone+listtwo # [1, 2, 3, 4, 5, 6]

"""merge each bucket of two lists into larger chunk"""
duct={'thread-9': [103.12, 48.12, 37.9, 19.07, 26.55, 21.11, 24.77, 23.35, 22.45, 21.12], 'thread-8': [102.73, 41.07, 26.97, 31.99, 21.15, 23.8, 22.72, 22.15, 23.69, 29.61], 'thread-7': [101.57, 41.25, 23.5, 28.46, 27.1, 19.77, 24.8, 22.52, 22.78, 26.64], 'thread-6': [103.38, 59.5, 28.35, 28.12, 20.85, 24.3, 22.59, 23.42, 23.08, 19.58], 'thread-5': [103.58, 53.61, 32.16, 21.24, 24.98, 21.2, 25.21, 23.92, 21.74, 21.63], 'thread-4': [103.26, 54.87, 32.27, 25.61, 22.19, 23.12, 23.08, 23.04, 20.04, 20.94], 'thread-3': [103.28, 40.37, 23.33, 32.89, 22.39, 22.07, 23.03, 21.67, 22.82, 29.08], 'thread-2': [103.5, 42.51, 32.38, 28.44, 24.3, 21.84, 23.5, 23.77, 23.76, 22.4], 'thread-1': [103.36, 41.91, 36.85, 22.21, 22.85, 23.64, 22.41, 24.52, 21.52, 26.1], 'thread-0': [104.01, 39.52, 32.15, 28.62, 19.49, 24.94, 22.36, 25.77, 25.26, 23.2]}

print "input dictionary:",duct
print "expected output:"
num_buckets=10
bucket_size=1
for i in range(num_buckets):
    chunks_bucket_i = []
    for j in range(len(duct)):
        time_list = duct.get("thread-{}".format(j))
        chunks_bucket_i += time_list[i*bucket_size : (i+1)*bucket_size]
    print chunks_bucket_i
# output: [1,2,3,6,5,4],[4,5,6,3,2,1]

"""python zip would only group by 1 bucket-size"""
# print "zip output:", zip(duct["thread-0"], duct["thread-1"])

"""python itertools.islice???"""


