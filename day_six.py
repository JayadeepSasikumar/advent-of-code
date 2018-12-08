from math import sqrt
import os

import numpy as np

from config import DATA_DIR

LARGE_DISTANCE = 100000

def _get_input_list(input_file_name):
    input_data_file = os.path.join(DATA_DIR, input_file_name)
    with open(input_data_file, 'r') as fp:
        input_data = [tuple(line.strip().split(', ')) for line in fp]
    input_data = [(int(x), int(y)) for (x, y) in input_data]
    return np.array(input_data)

def get_distance(x1, y1, x2, y2):
	x_diff = abs(x1 - x2)
	y_diff = abs(y1 - y2)
	return x_diff + y_diff

def get_area_map(coordinates):
	"""
	Returns a numpy array, with each cell having the closest location
	to it recorded in it.
	"""

	def _get_nearest_location(row, column):
		"""
		"""
		duplicate_found = False
		min_distance = LARGE_DISTANCE
		min_distance_location_id = -2
		if [row, column] in coordinates.tolist():
			return area_map[row][column]
		for location_id, [x, y] in enumerate(coordinates):
			distance = get_distance(x, y, row, column)
			if distance < min_distance:
				duplicate_found = False
				min_distance = distance
				min_distance_location_id = location_id
			elif min_distance == distance:
				duplicate_found = True
		if duplicate_found:
			min_distance_location_id = -1
		return min_distance_location_id

	row_max, column_max = coordinates.max(axis = 0)
	area_map = np.zeros((row_max + 1, column_max + 1))
	for location_id, [row, column] in enumerate(coordinates):
		area_map[row][column] = location_id
	for row in range(row_max + 1):
		for column in range(column_max + 1):
			area_map[row][column] = _get_nearest_location(row, column)
	return area_map

def get_unbounded_locations(area_map, coordinates):
	"""
	Takes in the area map and returns the locations which are
	unbounded.
	"""
	x_max, y_max = coordinates.max(axis=0)
	unbounded_locations = area_map[:, 0].tolist() + area_map[0, :].tolist() + \
							area_map[x_max, :].tolist() + \
							area_map[:, y_max].tolist()
	unbounded_locations = list(set(unbounded_locations))
	return unbounded_locations

def get_bounded_area_dict(area_map, coordinates, unbounded_locations):
	"""
	Returns a dict with the relevant locations and their respective
	areas as keys and values.
	"""
	bounded_area_dict = {}
	for location_id, [x, y] in enumerate(coordinates):
		if location_id in unbounded_locations:
			continue
		bounded_area_dict[location_id] = (area_map == location_id).sum()
	return bounded_area_dict

def get_connected_area(coordinates, max_distance):
	"""
	Returns a numpy array with all cells in it that has the sum of
	distances to all the locations below max_distance.
	"""
	def is_connected(row, column):
		total_distance = 0
		for location_id, [x, y] in enumerate(coordinates):
			total_distance += get_distance(x, y, row, column)
		return total_distance < max_distance

	row_max, column_max = coordinates.max(axis = 0)
	connected_area = np.zeros((row_max + 1, column_max + 1))
	for row in range(row_max + 1):
		for column in range(column_max + 1):
			connected_area[row][column] = is_connected(row, column)
	return connected_area

def one(input_file_name='day_six.txt'):
	coordinates = _get_input_list(input_file_name)
	area_map = get_area_map(coordinates)
	unbounded_locations = get_unbounded_locations(area_map, coordinates)
	bounded_area_dict = get_bounded_area_dict(area_map, coordinates,
												unbounded_locations)
	return max(bounded_area_dict.values())

def two(input_file_name='day_six.txt'):
	coordinates = _get_input_list(input_file_name)
	connected_area = get_connected_area(coordinates, 10000)
	return connected_area.sum()
