import os
import re

import numpy as np

from config import DATA_DIR

def _parse_claim(input_line):
	"""
	Parses a claim of the format "#1305 @ 400,523: 25x10" and returns
	the claim details as a dict with ['id', 'x', 'y', 'w', 'h'] as the
	keys.

	Inputs -
		input_line - a claim of format "#id @ x,y: wxh"

	Returns -
		claim_details - a dict with ['id', 'x', 'y', 'w', 'h'] as the
			keys, and their respective values.
	"""
	claim_keys = ['id', 'x', 'y', 'w', 'h']
	claim_details = re.compile(r'[#@,:x]+').split(input_line)
	claim_details.remove('')
	claim_details = [int(detail.strip()) for detail in claim_details]
	claim_dict = dict([(claim_keys[ix], claim_details[ix])
						for ix, _ in enumerate(claim_details)])
	return claim_dict

def _get_input_list(input_file_name):
	input_data_file = os.path.join(DATA_DIR, input_file_name)
	with open(input_data_file, 'r') as fp:
		input_data = [_parse_claim(line.strip()) for line in fp]
	return input_data

def _get_fabric_with_claims(claims):
	"""
	Gets the claims, iterates over them, and mark the fabric with the
	possible overlaps. Any overlap is marked with a -1.

	Inputs -
		claims - a list of dicts, each dict representing a claim. Same
			dict as returned by _parse_claim().

	Returns -
		fabric - an np.array with claim_id in each square inch and
			-1 in overlapping areas.
	"""
	fabric = np.zeros((1000, 1000))
	for claim in claims:
		x, y, w, h = claim['x'], claim['y'], claim['w'], claim['h']
		patch = fabric[x: x + w, y: y + h]
		patch[patch != 0] = -1
		patch[patch == 0] = claim['id']
	return fabric

def one():
	claims = _get_input_list('day_three.txt')
	fabric = _get_fabric_with_claims(claims)
	return (fabric == -1).sum()

def two():
	claims = _get_input_list('day_three.txt')
	fabric = _get_fabric_with_claims(claims)
	for claim in claims:
		x, y, w, h = claim['x'], claim['y'], claim['w'], claim['h']
		patch = fabric[x: x + w, y: y + h]
		overlapping_square_inches = (patch == -1).sum()
		if not overlapping_square_inches:
			return claim['id']
