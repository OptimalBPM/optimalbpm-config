"""
This process file is a part of the Optimal BPM Python parsing testing,
It is neither runnable or thought of as a example.
"""

"""Get data from a data source"""
dataset = qal.merge_datasets(get_data("000000000000000000001234"))
"""Try and query the database"""
qal.query(get_data("56b913fb5552e1ad238e1498"))