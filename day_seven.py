import os
import string

import networkx as nx
import numpy as np

from collections import defaultdict

from config import DATA_DIR

def get_instructions(input_file_name):
    """
    Takes in the input file name where each line is of the format:
        "Step X must be finished before step Y can begin."
    Returns a list of tuples, each tuple of the format:
        (task, prerequisite)
    For the example above, it would be (X, Y)

    Input -
        input_file_name - the name of the input file

    Returns -
        instructions - a list of tuples, each tuple of the format:
            (task, prerequisite)
    """
    def _parse_instruction(instruction_line):
        return (instruction_line[-3], instruction_line[1])

    input_data_file = os.path.join(DATA_DIR, input_file_name)
    with open(input_data_file, 'r') as fp:
        instructions = [_parse_instruction(line.strip().split())
                        for line in fp]
    return instructions

def get_tasks_order(graph):
    """
    Takes in the requirements of tasks and returns the order in which
    the tasks need to be executed.

    Input -
        graph - a networkx directed graph representing the tasks and
            their dependencies. An edge from X to Y signifies that Y
            is a prerequisite for X.

    Returns -
        tasks_order - a string which specifies the order in which the
            tasks need to be executed.
    """
    tasks_order = ""
    tasks = [task for task in graph.nodes]
    tasks.sort()
    while tasks:
        for task in tasks:
            if not graph[task]:
                tasks_order += task
                tasks.remove(task)
                graph.remove_node(task)
                break
    return tasks_order

def get_instructions_graph(instructions):
    """
    Builds and returns a networkx DiGraph

    Input - 
        instructions - a list of tuples, each tuple is of the format
            (task, prerequisite).

    Returns -
        graph - a networkx directed graph representing the tasks and
            their dependencies. An edge from X to Y signifies that Y
            is a prerequisite for X.
    """
    graph = nx.DiGraph()
    graph.add_edges_from(instructions)
    return graph

def get_task_times(graph, extra_time):
    """
    Returns a dict with tasks as keys and the respective times taken
    for their completion as values.

    Inputs -
        graph - a networkx directed graph representing the tasks and
            their dependencies. An edge from X to Y signifies that Y
            is a prerequisite for X.
        extra_time - int, a minimum common time taken for every task
            (in seconds).

    Returns - 
        task_times - a dict with tasks as keys and the respective times
            taken for their completion as values.
    """
    tasks = [task for task in graph.nodes]
    task_times = {task: ord(task) - 64 + extra_time for task in tasks}
    return task_times

def get_time_of_completion(graph, task_times, workers):
    """
    Inputs -
        graph - a networkx directed graph representing the tasks and
            their dependencies. An edge from X to Y signifies that Y
            is a prerequisite for X.
        task_times - dict, of format {task: time taken}
        workers - int, number of workers working on the whole project.

    Returns -
        overall_time - int, the overall time in seconds in which the
            work would be completed.
    """
    def _get_earliest_start_times(graph, task_times):
        """
        Inputs -
            graph, task_times - as obtained by parent function.

        Returns -
            earliest_start_times - dict, of format {task: est}
        """
        def _get_est(task):
            """
            Returns the earliest starting time possible for a task.
            """
            est = 0
            if not graph[task]:
                return est
            for dependent_task in graph[task]:
                est += task_times[dependent_task] + _get_est(dependent_task)
            return est

        tasks = [task for task in graph.nodes]
        earliest_start_times = {task: _get_est(task) for task in tasks}
        return earliest_start_times

    def _get_task_queues(graph, task_times, workers):
        """
        Inputs - same as the parent function(get_time_of_completion()).

        Returns -
            task_queues - np.charrarray, represents which task each
                worker is working on at any given second; of the shape
                (maximum_time, workers).
        """
        def _get_free_worker(task):
            try:
                est = graph.nodes[task]['est']
            except KeyError:
                return work_till_times.argmin()
            else:
                temp_work_till_times = work_till_times.copy()
                temp_work_till_times[temp_work_till_times < est] = est
                return temp_work_till_times.argmin()

        maximum_time = sum(task_times.values())
        task_queues = np.chararray((maximum_time, workers))
        work_till_times = np.zeros(workers)
        reverse_graph = graph.reverse()
        task_queues[:] = b'-'
        while graph.nodes:
            ready_tasks = [task for task in graph.nodes if not graph[task]]
            ready_tasks.sort(key=lambda x: graph.nodes[x].get('est', 0))
            for task in ready_tasks:
                worker= _get_free_worker(task)
                start_time = graph.nodes[task].get('est', work_till_times[worker])
                end_time = start_time + graph.nodes[task]['duration']
                work_till_times[worker] = end_time
                for dependent_task in reverse_graph[task]:
                    est = graph.nodes[dependent_task].get('est', 0)
                    if end_time > est:
                        graph.nodes[dependent_task]['est'] = end_time
                task_queues[int(start_time): int(end_time), worker] = task
                graph.remove_node(task)
        return task_queues
    task_queues = _get_task_queues(graph, task_times, workers)
    tasks_per_second = (task_queues != b'-').sum(axis=1)
    overall_time = (tasks_per_second > 0).sum()
    return overall_time

def one(input_file_name='day_seven.txt'):
    instructions = get_instructions(input_file_name)
    instructions_graph = get_instructions_graph(instructions)
    tasks_order = get_tasks_order(instructions_graph)
    return tasks_order

def two(input_file_name='day_seven.txt', workers=5, extra_time=60):
    instructions = get_instructions(input_file_name)
    instructions_graph = get_instructions_graph(instructions)
    task_times = get_task_times(instructions_graph, extra_time)
    nx.set_node_attributes(instructions_graph, task_times, 'duration')
    overall_time = get_time_of_completion(instructions_graph,
                                            task_times, workers)
    return overall_time
