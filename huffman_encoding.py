#!/usr/bin/env python


import array
import json

sample_dict = {}
sample_dict['e'] = 3
sample_dict['e'] += 1
sample_dict['f'] = 1
sample_dict['char_count'] = 100

# converts integer to binary string
result = "{0:08b}".format(6)
print result

# converts binary strings to integers
data = array.array('B')
data.append(int('10001000', 2))
data.append(int('10000001', 2))
print data
f = open('out.txt', 'wb')
f.write(data)
f.close()

# writes dictionary info to a file
with open("jsonfile.json", "w") as char_dict:
    json.dump(sample_dict, char_dict)
char_dict.close()

# pull dictionary info from a file
with open("jsonfile.json", "r") as new_dict:
    new_data = json.load(new_dict)
    print(new_data['char_count'])
new_dict.close()
