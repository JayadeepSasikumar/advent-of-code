import os

from config import DATA_DIR

def _get_input_list(input_file_name):
	input_data_file = os.path.join(DATA_DIR, input_file_name)
	with open(input_data_file, 'r') as fp:
		input_data = [int(line) for line in fp]
	return input_data

def one():
	input_data = _get_input_list('day_one.txt')
	return sum(input_data)

def two():
	input_data = _get_input_list('day_one.txt')
	reached_values = [0]
	current_value = 0
	overall_idx = 0
	data_len = len(input_data)
	import ipdb; ipdb.set_trace()
	while True:
		current_idx = overall_idx % data_len
		current_value += input_data[current_idx]
		if not current_value in reached_values:
			reached_values.append(current_value)
			overall_idx += 1
		else:
			break
	return current_value
