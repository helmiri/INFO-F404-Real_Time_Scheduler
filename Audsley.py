from Scheduler import *


def audsley(tasks):
    """ Implementation of Audsley's algorithm. Returns True if there exists a feasible FTP assignment
            args: - tasks: a copy of the list of Task objects because the list will be modified
    """   

    result = False
    if len(tasks) < 2:
        return True # We've reached the end, no task has missed its deadline

    for item in tasks:
        item.set_priority(len(tasks)) # Assign to this item the lowest priority (bigger number, smaller priority)
        item.set_soft(False) # Deadline isn't soft

        # Assign priorities to the other tasks and clear their internal information from previous executions
        for i in range(len(tasks)):
            tasks[i].reset_counter()
            tasks[i].clear_scheduled()
            if item == tasks[i]:
                continue
            tasks[i].set_priority(i)
            tasks[i].set_soft(True)

        scheduler = Scheduler(tasks)
        if scheduler.schedule():
            # No deadline has been missed, proceed with the algorithm
            tasks.remove(item)
            result = audsley(tasks.copy())
            if result:
                return True  # A feasible FTP assignment has been found
    return result
