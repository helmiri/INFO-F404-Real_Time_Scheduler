import matplotlib.pyplot as plot
from matplotlib.pyplot import figure

class GanttPlot:

    def __init__(self, data):
        """
            data: List of lists of tuples where each list is the execution
                  of a task and each tuple within that list is such that (T, D) where:
                    T = Start time of the job
                    D = Duration of the job

        """
        self.tasks = data
        self.tasks_num = len(data)

        self.bar_height = 4
        self.tick_step = 4
        self.tick_start = 2

        self.figure, self.axes = plot.subplots()
        # Labels
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Tasks')

        # Color and format
        self.colors = plot.rcParams['axes.prop_cycle'].by_key()['color']
        self.grid_style = ["grey", '--', 0.5, 0.8]

        self.populate_data()
        self.plot_format()

    def plot_format(self):

        # Set ticks and labels on y-axis
        self.axes.set_yticks([i for i in range(
            self.tick_start, self.tasks_num * self.tick_step, self.tick_step)])
        self.axes.set_yticklabels(
            ["Task {0}".format(i + 1) for i in range(self.tasks_num)])

        # Display range
        self.axes.set_ylim(bottom=1, top=self.tasks_num * self.tick_step)
        
        # Set ticks on x-axis to display each tick
        # Get highest x value after populating plot
        limit = int(self.axes.get_xlim()[1]) + 1
        self.axes.set_xticks([i for i in range(limit)])
        self.axes.set_xlim([0, limit])

        # Draw custom grid offset by 5 units on the y axis
        for i in range(self.tasks_num + 1):
            plot.axhline(y=i * self.tick_step,
                         color=self.grid_style[0], linestyle=self.grid_style[1], alpha=self.grid_style[2], linewidth=self.grid_style[3])

        for i in range(limit):
            plot.axvline(x=i, color=self.grid_style[0], linestyle=self.grid_style[1],
                         alpha=self.grid_style[2], linewidth=self.grid_style[3])
        
        plot.xlim(0, 20) # Set view limit
        return

    def populate_data(self):
        # Plots every job
        for i in range(self.tasks_num):
            self.axes.broken_barh(
                self.tasks[i], (i * self.tick_step, self.bar_height), facecolor=self.colors[i % len(self.colors)])

        return

    def show(self):
        plot.show()

