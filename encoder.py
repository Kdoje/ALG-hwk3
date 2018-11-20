#!/usr/bin/env python

import array
import json
import sys
from PriorityQueue import PriorityQueue

class h_node:
    left_node = None
    right_node = None
    frequency = 0
    cur_char = None

    def __init__(self, left_node, right_node, frequency, cur_char):
        # type: (self, h_node, h_node, int, chr) -> h_node
        self.cur_char = cur_char
        self.left_node = left_node
        self.right_node = right_node
        self.frequency = frequency

    def __str__(self):
        to_print = "char:{} frequency:{} ".format(self.cur_char, self.frequency)

        if self.left_node:
            to_print += "l_node: {} ".format(self.left_node.cur_char)
        if self.right_node:
            to_print += "r_node: {} ".format(self.right_node.cur_char)
        return to_print


def get_char_freq(file_name):
    """
    gets the sorted list of character frequencies
    :param file_name: the file to parse through
    :type file_name: str
    :return: the huffman tree
    """
    char_frequency = {}
    char_count = 0

    with open(file_name) as to_encode:
        cur_char = to_encode.read(1)
        while cur_char:
            if char_frequency.has_key(cur_char):
                char_frequency[cur_char] += 1
            else:
                char_frequency[cur_char] = 1
            char_count += 1
            cur_char = to_encode.read(1)
    print char_frequency
    # create the huffman list of nodes sorted by count
    nodes = PriorityQueue()

    # adds the initial nodes to the list
    for node_char, node_freq in char_frequency.iteritems():
        nodes.put(h_node(None, None, node_freq, node_char), node_freq)

    # create the tree of nodes required to get the character codes
    while nodes.count() > 1:
        # get the two smallest nodes
        h_node_a=nodes.get()
        h_node_b=nodes.get()
        freq_sum=h_node_a.frequency+h_node_b.frequency
        nodes.put(h_node(h_node_a, h_node_b, freq_sum, None), freq_sum)

    return nodes.get()

def get_char_code(h_tree, code_string, char_dict):
    """
    this is a recursive function that will fill out the dictionary
    :param h_tree: the root node to find the character codes from
    :type h_tree: h_node
    :return: None
    """
    if not h_tree.left_node and not h_tree.right_node:
        char_dict[h_tree.cur_char]=code_string
        return

    if h_tree.right_node:
        get_char_code(h_tree.right_node, code_string + '1', char_dict)
    if h_tree.left_node:
        get_char_code(h_tree.left_node, code_string + '0', char_dict)


def encode(file_name):
    """
    :param file_name: the file to encode
    :type file_name: str
    :return:
    """
    h_tree=get_char_freq(file_name)
    char_dict = {}
    get_char_code(h_tree, '', char_dict)
    print char_dict

def decode(file_name):
    """
    :param file_name: the file to decode
    :type file_name: file
    :return:
    """


# use enc to encode and dec to decode
if __name__ == "__main__":
    if len(sys.argv) == 3:
        if str(sys.argv[1]) == "enc":
            encode(sys.argv[2])
        if str(sys.argv[1]) == "dec":
            decode(sys.argv[2])
    else:
        print "Please give 2 argument of [enc/dec] [file_name]\n"
