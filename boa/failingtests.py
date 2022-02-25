#!/usr/bin/env python3

with open("output/part-r-00000") as f:
    s = f.readline()
    while s is not None and len(s.strip()) > 0:
        parts = s.split(' = ')

        first_nums = parts[0].split('][')
        test_name = first_nums[1]
        first_nums = first_nums[-3].translate({ord('.'): None, ord('p'): None, ord('y'): None, ord(']'): None}).split('-')[-5:]

        second_nums = parts[1].translate({ord('{'): None, ord('}'): None, ord(' '): None, ord('\n'): None}).split(',')

        if 'proc' not in second_nums and 'oo' not in second_nums and 'func' not in second_nums and 'imp' not in second_nums and 'mixed' not in second_nums:
            if first_nums != second_nums:
                print(test_name + ': no match, found: ' + '-'.join(second_nums))

        s = f.readline()