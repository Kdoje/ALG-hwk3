#!/usr/bin/env python

import array
import json
import sys
from PriorityQueue import PriorityQueue

compression_file = "compressionInfo.json"
file_dict_str = "char_dict"
file_length_str = "file_length"


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
    :return: the huffman tree and char count
    """
    char_frequency = {}

    with open(file_name) as to_encode:
        cur_char = to_encode.read(1)
        while cur_char:
            if char_frequency.has_key(cur_char):
                char_frequency[cur_char] += 1
            else:
                char_frequency[cur_char] = 1
            cur_char = to_encode.read(1)

    # create the huffman list of nodes sorted by count
    nodes = PriorityQueue()

    # adds the initial nodes to the list
    for node_char, node_freq in char_frequency.iteritems():
        nodes.put(h_node(None, None, node_freq, node_char), node_freq)

    # create the tree of nodes required to get the character codes
    while nodes.count() > 1:
        # get the two smallest nodes
        h_node_a = nodes.get()
        h_node_b = nodes.get()
        freq_sum = h_node_a.frequency + h_node_b.frequency
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
        char_dict[h_tree.cur_char] = code_string
        return

    if h_tree.right_node:
        get_char_code(h_tree.right_node, code_string + '1', char_dict)
    if h_tree.left_node:
        get_char_code(h_tree.left_node, code_string + '0', char_dict)


def gen_compressed_file(char_dict, file_name):
    """
    This will parse through the file and create the string, then
    the actual binary of the file
    :param char_dict: the replacment policy
    :param file_name: the file to parse through
    :return: the original compressed string
    """
    # create the string of 1s and 0s to be converted into bytes
    compressed_string = ""
    with open(file_name) as to_encode:
        cur_char = to_encode.read(1)
        while cur_char:
            compressed_string += char_dict[cur_char]
            cur_char = to_encode.read(1)

    # we want to return the length of the original compressed
    # string to decode it properly

    # create the array of ints needed to store the compressed file
    with open("compressed.txt", "w") as comp:
        cur_string = ''
        file_contents = array.array('B')

        for c in compressed_string:
            cur_string += c
            if len(cur_string) == 8:
                file_contents.append(int(cur_string, 2))
                # reset cur string
                cur_string = ''

        # once finished we need to make sure the tail end of
        # cur string is added to the file
        while len(cur_string) < 8:
            cur_string += '0'
        file_contents.append(int(cur_string, 2))
        file_contents.tofile(comp)

        return compressed_string


def encode(file_name):
    """
    :param file_name: the file to encode
    :type file_name: str
    :return:
    """
    h_tree = get_char_freq(file_name)
    char_dict = {}
    get_char_code(h_tree, '', char_dict)
    print char_dict
    compressed_string = gen_compressed_file(char_dict, file_name)


    # now we need to get the data into a json
    # first reverse the dictionary so when we parse through the file
    # we can get the character from the code
    char_dict = {v: k for k, v in char_dict.iteritems()}
    file_len = len(compressed_string)
    print file_len
    print char_dict

    # now get the encoding information into the json
    with open(compression_file, "w") as comp:
        info = {file_dict_str: char_dict,
                file_length_str: file_len}
        json.dump(info, comp)


def decode(file_name):
    """
    :param file_name: the file to decode
    :type file_name: str
    :return:
    """
    # need to pull the info out of compressionInfo
    info = {}
    char_dict = {}
    output_file = "decompressed.txt"

    with open(compression_file, "r") as comp:
        info = json.load(comp)
    file_len = info[file_length_str]
    char_dict = info[file_dict_str]

    # now we want to get a string representation of the file
    # with ones and zeros
    compressed_string = ""

    with open("compressed.txt", "r") as to_decode:
        cur_char = to_decode.read(1)
        while cur_char:
            compressed_string += "{0:08b}".format(ord(cur_char))
            cur_char = to_decode.read(1)

    bit_count = 0
    cur_string = ""
    with open(output_file, "w") as output_file:
        while bit_count < file_len:
            cur_string += compressed_string[bit_count]
            # if the dictionary contains the current string
            # add the character to the output file
            if cur_string in char_dict.keys():
                output_file.write(char_dict[cur_string])
                cur_string=""
            bit_count+=1



# use enc to encode and dec to decode
if __name__ == "__main__":
    if len(sys.argv) == 3:
        if str(sys.argv[1]) == "enc":
            encode(sys.argv[2])
        if str(sys.argv[1]) == "dec":
            decode(sys.argv[2])
    else:
        print "Please give 2 argument of [enc/dec] [file_name]\n"
