import os

import numpy as np

from datetime import datetime

from config import DATA_DIR


def _parse_info(input_line):
    """
    Parses an input line of the format "[1518-05-28 00:59] wakes up"
    and returns the parsed information as a dict.

    Inputs -
        input_line - a claim of format "[datetime] guard-action".

    Returns -
        security_action - a dict with ['date_time', 'action_type',
            'security_id'] as the possible keys.
    """
    date_time_str, guard_info = input_line.split('] ')
    info = {
        'date_time': datetime.strptime(date_time_str, '[%Y-%m-%d %H:%M'),
    }
    if 'wakes' in guard_info:
        info['action_type'] = 'wakes up'
    elif 'falls' in guard_info:
        info['action_type'] = 'sleeps'
    else:
        guard_id = guard_info.split()[1][1:]
        info['guard_id'] = int(guard_id)
    return info

def _get_input_list(input_file_name):
    input_data_file = os.path.join(DATA_DIR, input_file_name)
    with open(input_data_file, 'r') as fp:
        input_data = [_parse_info(line.strip()) for line in fp]
    return input_data

def get_sorted_security_actions(input_file_name):
    security_actions = _get_input_list(input_file_name)
    security_actions.sort(key=lambda x: x['date_time'])
    return security_actions

def get_guards_sleep_times(security_actions):
    """
    Returns a dict with guard id as the key and that guard's sleeping
    pattern as the value.

    Inputs -
        security_actions - a list of dicts, each dict representing a
            guard's action, sorted by date_time key of the dicts.

    Returns -
        guards_sleep_times - a dict with guard id as the key and a
            numpy array of length 60 as the value. The value in each
            column gives the number of times the guard has slept in
            that minute (of any day).
    """
    guards_sleep_times = {}
    current_guard_id = 0
    sleeping_minute = 0
    waking_up_minute = 0
    for action in security_actions:
        if 'guard_id' in action:
            current_guard_id = action['guard_id']
        if 'action_type' in action:
            guard_sleep_times = guards_sleep_times.get(current_guard_id,
                                                        np.zeros(60))
            if action['action_type'] == 'sleeps':
                sleeping_minute = action['date_time'].minute
            elif action['action_type'] == 'wakes up':
                waking_up_minute = action['date_time'].minute
                guard_sleep_times[sleeping_minute: waking_up_minute] += 1
                guards_sleep_times[current_guard_id] = guard_sleep_times
    return guards_sleep_times

def _get_key_with_max_value(dictionary):
    max_key = 0
    max_value = 0
    for key, value in dictionary.items():
        if value > max_value:
            max_key = key
            max_value = value
    return max_key

def get_heaviest_sleeper(guards_sleep_times):
    """
    Returns the id of the guard who has slept the most minutes among
    all the guards.

    Inputs -
        guards_sleep_times - a dict with guard id as the key and a
            numpy array of length 60 as the value. The value in each
            column gives the number of times the guard has slept in
            that minute (of any day). (Same format as returned by
            get_guards_sleep_times()).

    Returns -
        heaviest_sleeper - the id of the guard who slept the most
            across the entire time period, among all the guards.
    """
    total_sleeping_times = {guard_id: sleep_times.sum()
                                    for guard_id, sleep_times
                                            in guards_sleep_times.items()}
    heaviest_sleeper = _get_key_with_max_value(total_sleeping_times)
    return heaviest_sleeper

def get_routine_sleeper(guards_sleep_times):
    """
    Returns the minute in which a particular guard has slept the most.

    Inputs -
        guards_sleep_times - same format as returned by
            get_guards_sleep_times().

    Returns -
        routine_sleeper - the id of the guard who slept most frequently
            at any one particular minute across the entire time period,
            among all the guards.
    """
    routine_days = {guard_id: sleep_times.max()
                            for guard_id, sleep_times
                                    in guards_sleep_times.items()}
    routine_sleeper = _get_key_with_max_value(routine_days)
    return routine_sleeper

def get_sleepiest_minute(guards_sleep_times, guard_id):
    """
    Returns the minute in which a particular guard has slept the most.

    Inputs -
        guards_sleep_times - same format as returned by
            get_guards_sleep_times().
        guard_id - id of the guard for which the info is required.

    Returns -
        sleepiest_minute - the minute in which the guard has slept the
            most.
    """
    return guards_sleep_times[guard_id].argmax()

def one():
    security_actions = get_sorted_security_actions('day_four.txt')
    guards_sleep_times = get_guards_sleep_times(security_actions)
    heaviest_sleeper = get_heaviest_sleeper(guards_sleep_times)
    sleepiest_minute = get_sleepiest_minute(guards_sleep_times, heaviest_sleeper)
    return heaviest_sleeper * sleepiest_minute

def two():
    security_actions = get_sorted_security_actions('day_four.txt')
    guards_sleep_times = get_guards_sleep_times(security_actions)
    routine_sleeper = get_routine_sleeper(guards_sleep_times)
    sleepiest_minute = get_sleepiest_minute(guards_sleep_times, routine_sleeper)
    return routine_sleeper * sleepiest_minute
