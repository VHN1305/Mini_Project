import sys

def read_input():
    num_thesises, num_teachers, num_councils = map(int, input().split())

    a, b, c, d, e, f = map(int, input().split())
    s, g, q = [], [], []
    for _ in range(num_thesises):
        row = list(map(int, input().split()))
        s.append(row)

    for _ in range(num_thesises):
        row = list(map(int, input().split()))
        g.append(row)

    q = list(map(int, input().split()))

    return num_thesises, num_teachers, num_councils, a, b, c, d, e, f, s, g, q
def link_to_small_input():
    test_case_1 = 'Dataset\Small\input_6_4_2.txt'
    test_case_2 = 'Dataset\Small\input_8_4_3.txt'
    test_case_3 = 'Dataset\Small\input_10_4_3.txt'
    test_case_4 = 'Dataset\Small\input_10_6_3.txt'
    test_case_5 = 'Dataset\Small\input_12_6_4.txt'
    return test_case_1, test_case_2, test_case_3, test_case_4, test_case_5

def link_to_medium_input():
    test_case_1 = 'Dataset\Medium\input_12_8_4.txt'
    test_case_2 = 'Dataset\Medium\input_14_8_4.txt'
    test_case_3 = 'Dataset\Medium\input_14_10_5.txt'
    test_case_4 = 'Dataset\Medium\input_16_10_6.txt'
    test_case_5 = 'Dataset\Medium\input_16_12_6.txt'
    return test_case_1, test_case_2, test_case_3, test_case_4, test_case_5

def link_to_large_input():
    test_case_1 = 'Dataset\Large\input_18_12_6.txt'
    test_case_2 = 'Dataset\Large\input_18_14_8.txt'
    test_case_3 = 'Dataset\Large\input_20_14_8.txt'
    test_case_4 = 'Dataset\Large\input_24_14_10.txt'
    test_case_5 = 'Dataset\Large\input_24_16_10.txt'
    return test_case_1, test_case_2, test_case_3, test_case_4, test_case_5

def link_to_extra_large_input():
    test_case_1 = 'Dataset\Extra-large\input_26_16_12.txt'
    test_case_2 = 'Dataset\Extra-large\input_30_18_12.txt'
    test_case_3 = 'Dataset\Extra-large\input_40_18_12.txt'
    test_case_4 = 'Dataset\Extra-large\input_40_20_14.txt'
    test_case_5 = 'Dataset\Extra-large\input_50_24_16.txt'
    return test_case_1, test_case_2, test_case_3, test_case_4, test_case_5


def input_data():
    input = []
    test_case_1, test_case_2, test_case_3, test_case_4, test_case_5 = link_to_small_input()
    test_case_6, test_case_7, test_case_8, test_case_9, test_case_10 = link_to_medium_input()
    test_case_11, test_case_12, test_case_13, test_case_14, test_case_15 = link_to_large_input()
    test_case_16, test_case_17, test_case_18, test_case_19, test_case_20 = link_to_extra_large_input()
    input = [test_case_1, test_case_2, test_case_3, test_case_4, test_case_5, test_case_6, 
             test_case_7, test_case_8, test_case_9, test_case_10, test_case_11, test_case_12, 
             test_case_13, test_case_14, test_case_15, test_case_16, test_case_17, test_case_18,
             test_case_19, test_case_20]
    # check if not win32, add . to the path and convert to linux path
    if sys.platform != 'win32':
        for i in range(len(input)):
            input[i] = '..\\' + input[i]
            input[i] = input[i].replace('\\', '/')
        
    return input

data_input = input_data()