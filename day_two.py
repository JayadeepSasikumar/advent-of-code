import os

from collections import Counter

from config import DATA_DIR


def _get_input_list(input_file_name):
	input_data_file = os.path.join(DATA_DIR, input_file_name)
	with open(input_data_file, 'r') as fp:
		input_data = [line.strip() for line in fp]
	return input_data

def one():
	box_ids = _get_input_list('day_two.txt')
	box_ids_counters = [Counter(item) for item in box_ids]
	doubles = [box_ids[ix] for ix, counter in enumerate(box_ids_counters)
			   if 2 in counter.values()]
	triples = [box_ids[ix] for ix, counter in enumerate(box_ids_counters)
			   if 3 in counter.values()]
	checksum = len(doubles) * len(triples)
	return checksum

def two():
	def _get_similar_ids(box_ids):
		for ix, box_id in enumerate(box_ids):
			for right_ix, right_box_id in enumerate(box_ids):
				if ix == right_ix:
					continue
				else:
					flag = False
					faulty_position = 0
					for char_ix in range(len(box_id)):
						if box_id[char_ix] != right_box_id[char_ix]:
							if not flag:
								flag = True  # First different letter spotted
								faulty_position = char_ix
							else:
								flag = False  # Second different letter spotted
								break
					if flag:
						return ix, right_ix, faulty_position

	def _get_new_label(box_ids, idx, faulty_position):
		new_label = box_ids[idx][:faulty_position] + \
					box_ids[idx][faulty_position+1:]
		return new_label

	box_ids = _get_input_list('day_two.txt')
	first_idx, second_idx, faulty_position = _get_similar_ids(box_ids)
	new_first_idx = _get_new_label(box_ids, first_idx, faulty_position)
	new_second_idx = _get_new_label(box_ids, second_idx, faulty_position)
	assert new_first_idx == new_second_idx
	return new_first_idx
