class Task:
    def __init__(self, task_id, offset, wcet, deadline, period):
        # Task info
        self.task_id = task_id
        self.offset = offset
        self.wcet = wcet
        self.deadline = deadline
        self.period = period

        self.is_soft = False
        self.priority = 0
        # Jobs released and correctly scheduled
        self.job_counter = 0
        self.scheduled_jobs = list()

    def is_dead_soft(self):
        return self.is_soft

    def set_soft(self, bool):
        self.is_soft = bool

    def set_priority(self, p):
        self.priority = p

    def get_priority(self):
        return self.priority

    def release_job(self):
        new_job = Job(self, self.job_counter)
        # Needed to give each job a unique ID used in their deadline computation
        self.job_counter += 1
        return new_job

    def get_wcet(self):
        return self.wcet

    def add_scheduled_job(self, job):
        self.scheduled_jobs.append(job)

    def get_offset(self):
        return self.offset

    def get_period(self):
        return self.period

    def clear_scheduled(self):
        self.scheduled_jobs.clear()

    def get_scheduled_jobs(self):
        return self.scheduled_jobs

    def get_deadline(self):
        return self.deadline

    def reset_counter(self):
        self.job_counter = 0

    def __lt__(self, other):
        return self.priority < other.get_priority()


class Job:

    def __init__(self, task, id):
        """
            args: - task: parent task
                  - id  : unique identifier (0-n)
        """
        self.id = id
        self.parent_task = task
        self.execution_remaining = task.get_wcet()

    def get_id(self):
        return self.id

    def get_priority(self):
        return self.parent_task.get_priority()

    def get_deadline(self):
        return self.parent_task.get_deadline()

    def get_task(self):
        return self.parent_task

    def get_period(self):
        return self.parent_task.get_period()

    def get_offset(self):
        return self.parent_task.get_offset()

    def is_soft(self):
        return self.parent_task.is_dead_soft()

    def is_deadline_missed(self, current_time):
        if self.is_soft():
            return False
        else:
            # offset + (id * period) will compute the period we're in. That's why we need the job ids from 0-n
            # + deadline to get where the deadline is in time
            # - execution_remaining - current_time allows us to know whether the job will finish its execution before the deadline or not.
            # If negative, the deadline is missed.
            return self.get_offset() + (self.id * self.get_period()) + self.get_deadline() - self.execution_remaining - current_time < 0

    def schedule(self):
        # Decreases the job's execution time and returns True if the job hasn't finished executing, False otherwise
        self.execution_remaining -= 1
        return self.execution_remaining != 0

    def finish_schedule(self, execution):
        self.parent_task.add_scheduled_job(execution)

    def __lt__(self, other):
        return self.parent_task < other.get_task()
