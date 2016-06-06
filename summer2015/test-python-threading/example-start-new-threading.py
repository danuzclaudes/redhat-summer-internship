#!/usr/bin/env python
import threading
import time

exitFlag = 0


class TestThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # invoke function defined outside of thread class, e.g. delete sequential
        print_time(self.name, 5, self.counter)
        print("Exiting " + self.name)


def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            thread_name.exit()
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1

    if __name__ == '__main__':
        """Create new threads"""
        thread1 = TestThread(1, "Thread-1", 5)
        thread2 = TestThread(2, "Thread-2", 5)
        """Start new Threads"""
        thread1.start()
        thread2.start()
        """Wait for thread2 to finish"""
        thread2.join()
        print("Exiting Main Thread")
"""
Output of using join
Starting Thread-1
Starting Thread-2
Thread-1: Wed Jun 17 15:36:06 2015
Thread-2: Wed Jun 17 15:36:06 2015
Thread-1: Wed Jun 17 15:36:11 2015
 Thread-2: Wed Jun 17 15:36:11 2015
Thread-1: Wed Jun 17 15:36:16 2015
 Thread-2: Wed Jun 17 15:36:16 2015
Thread-1: Wed Jun 17 15:36:21 2015
Thread-2: Wed Jun 17 15:36:21 2015
Thread-1: Wed Jun 17 15:36:26 2015
Exiting Thread-1
Thread-2: Wed Jun 17 15:36:26 2015
Exiting Thread-2
Exiting Main Thread

Output of not using join
Starting Thread-1
Starting Thread-2Exiting Main Thread

Thread-1: Wed Jun 17 15:49:23 2015
 Thread-2: Wed Jun 17 15:49:23 2015
Thread-1: Wed Jun 17 15:49:28 2015
 Thread-2: Wed Jun 17 15:49:28 2015
Thread-1: Wed Jun 17 15:49:33 2015
Thread-2: Wed Jun 17 15:49:33 2015
Thread-1: Wed Jun 17 15:49:38 2015
 Thread-2: Wed Jun 17 15:49:38 2015
Thread-1: Wed Jun 17 15:49:43 2015
Exiting Thread-1
 Thread-2: Wed Jun 17 15:49:43 2015
Exiting Thread-2
"""
