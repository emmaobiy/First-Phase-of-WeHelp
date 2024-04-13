def get_number(index):
    number_sequence = [0]
    value = 0
    
    for i in range(1, index+1):
        increment = 0
        if i % 3 == 0:
            increment = -1
        else:
            increment = 4
        value += increment
        number_sequence.append(value)

    print(number_sequence[index])

get_number(1)  # print 4
get_number(5)  # print 15
get_number(10)  # print 25
get_number(30)  # print 70
