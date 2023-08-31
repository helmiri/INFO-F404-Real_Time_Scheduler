from random import randint
import sys


class Generator:
    """
 Class that allows us to generate a number of tasks with their Offset, WCET, and Period in a given file.
    
    """

    def __init__(self, task_number, task_file, max_offset, max_wcet, max_period):
        self.max_period = max_period
        self.max_wcet = max_wcet
        self.max_offset = max_offset

        self.task_number = task_number
        self.task_file = task_file
        self.offset_list = []
        self.wcet_list = []
        self.period_list = []
        self.deadline_list = []

    def generate_all_data(self):
        self.generate_offset()
        self.generate_wcet()
        self.generate_deadline()
        self.generate_period()
        string_to_write = ""
        for task in range(self.task_number):
            string_to_write += str(self.offset_list[task]) + " " + \
                               str(self.wcet_list[task]) + " " + str(self.deadline_list[task]) + " " + str(
                self.period_list[task]) + "\n"
        return string_to_write

    def generate_offset(self):
        for i in range(self.task_number):
            self.offset_list.append(randint(0, self.max_offset))  # the offset is always 0

    def generate_wcet(self):
        for i in range(self.task_number):
            self.wcet_list.append(randint(1, self.max_wcet))

    def generate_period(self):
        for task in range(self.task_number):
            self.period_list.append(randint(self.deadline_list[task], self.max_period))

    def generate_deadline(self):
        for task in range(self.task_number):
            self.deadline_list.append(randint(self.wcet_list[task] + 1, self.max_period))

    def write_in_file(self):
        f = open(self.task_file, "w+")
        f.write(self.generate_all_data())
        f.close()


if len(sys.argv) != 6:
    print(
        "Error in the commandline :Python Generator.py task_number  task_file  max_offset  max_wcet  max_period ")
    exit()
f = Generator(int(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
f.write_in_file()
