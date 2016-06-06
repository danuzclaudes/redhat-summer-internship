#!/usr/bin/env python
from tests.foreman.performance.common.perf_candlepin import CandlepinPerfTest

import logging
import threading
import time


class PerfThread(threading.Thread):
    def __init__(self, threadID, threadName, sublist, time_result_dict):
        threading.Thread.__init__(self)
          
        self.threadID = threadID
        self.threadName=threadName
        self.sublist = sublist
        self.time_result_dict = time_result_dict
        self.logger = logging.getLogger('robottelo')

    def run(self):
        self.logger.info('---------------------------------')
        time.sleep(5)
        self.logger.debug('Start timing in thread {}'.format(self.threadID))
        for idx, uuid in enumerate(self.sublist):
            self.logger.debug('deletion attempt # {0} in thread {1}-uuid: {2}'.format(idx, self.threadID, uuid))
            # conduct one request by the id
            time_point = CandlepinPerfTest.single_delete(uuid)
            self.time_result_dict[self.threadName].append(time_point)
