from Gantt import *
from Scheduler import Scheduler
from Task import *
import Audsley
import sys


def execute_audsley(tasks):
    result = Audsley.audsley(tasks.copy())
    if not result:
        print("No feasible FTP assignment has been found")
        return

    tasks.sort()
    with open("audsley.txt", "w+") as file:
        for task in tasks:
            file.write("{0} {1} {2} {3}\n".format(task.get_offset(), task.get_wcet(), task.get_deadline(), task.get_period()))



def execute_scheduler(tasks):
    result = Audsley.audsley(tasks.copy())
    if not result:
        print("No feasible FTP assignment has been found")
        exit()
    scheduler = Scheduler(tasks)
    scheduler.schedule() # Audsley determined it is schedulable. No need to check.

    scheduled_jobs = list()
    for task in tasks:
        scheduled_jobs.append(task.get_scheduled_jobs())

    plot = GanttPlot(scheduled_jobs)
    plot.show()

    
if len(sys.argv) != 3:
    print("Usage: ./Main.py audsley|scheduler <task_file>")
    exit()

tasks = list()
with open(sys.argv[2], "r") as task_file:
    lines = task_file.readlines()
    id = 1
    for line in lines:
        task = line.split()
        tasks.append(Task(id, int(task[0]), int(task[1]), int(task[2]), int(task[3])))

if sys.argv[1] == "audsley":
    execute_audsley(tasks)
elif sys.argv[1] == "scheduler":
    execute_scheduler(tasks)
else:
    print("Argument not recognized\nUsage: ./Main.py audsley|scheduler <task_file>")
    

    

