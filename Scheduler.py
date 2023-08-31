import heapq
import numpy as np
from Task import *


class Time_Unit:
    """
        Class used to track time and job releases
    """

    def __init__(self, time):
        self.time = time
        self.releases = []  # Job releases at this timestep

    def get_time(self):
        return self.time

    def get_releases(self):
        """Returns a job for every Task in this time step"""
        for task in self.releases:
            yield task.release_job() 

    def add_release(self, task):
        # Add a task whose job releases occur at this time step
        self.releases.append(task)


class Scheduler:

    def __init__(self, task_list):
        """task_list: List of Task objects"""

        self.priority_queue = list()
        self.task_list = task_list
        offsets = [task_list[i].get_offset() for i in range(len(task_list))]
        periods = [task_list[i].get_period() for i in range(len(task_list))]
        self.time_array = np.array([Time_Unit(i) for i in range(
            max(offsets) + (2 * np.lcm.reduce(periods)))])  # Pre-generate the array
        self.init_time_array()

    def add_job(self, job):
        """Push a job into the priority queue"""

        heapq.heappush(self.priority_queue, job)

    def get_job(self):
        """Returns the job with highest priority. None if there are no more jobs in the queue"""

        if self.priority_queue != []:
            return heapq.heappop(self.priority_queue)
        else:
            return None

    def init_time_array(self):
        """Assignes job releases to the proper TimeUnit in the array"""

        for task in self.task_list:
            offset = task.get_offset()
            period = task.get_period()
            count = 0
            index = 0
            while offset + count * period < len(self.time_array):
                index = offset + count * period
                self.time_array[index].add_release(task)
                count += 1

    def schedule(self):
        """Executes the scheduling and returns False if any job misses its deadline, True otherwise"""

        current_job = None
        previous_job = None
        for time in self.time_array:

            # Add new job releases to the priority queue
            for release in time.get_releases():
                self.add_job(release)

            current_job = self.get_job()  # Pop the job with highest priority

            if previous_job is None:
                # Update it to ensure that no wrong information is carried over from previous iterations.
                start_time = time

            # Either the previous job finished scheduling, or a new one with higher priority is in the queue
            # Update its scheduled time before continuing
            if previous_job != current_job and previous_job is not None:
                previous_job.finish_schedule(
                    tuple((start_time.get_time(), time.get_time() - start_time.get_time())))
                start_time = time

            # No job to be scheduled. Update previous_job otherwise as iterations go on until we reach a new job release,
            # previous_job will still hold the reference to a job that has finished scheduling and the condition above
            # will pad the idle time with that job's execution
            if current_job is None:
                previous_job = None
                continue

            if current_job.is_deadline_missed(time.get_time()):
                return False

            if current_job.schedule():
                self.add_job(current_job)
            previous_job = current_job
        return True
