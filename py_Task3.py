def func(*data):
    middlename = []

    for name in data:
        if 2 <= len(name) <= 3:
            middlename.append(name[1])
        elif 4 <= len(name) <= 5:
            middlename.append(name[2])

   
    uniquename = None
    for char in middlename:
        if middlename.count(char) == 1:
            uniquename = char
            break

    if uniquename is None:
        print("沒有")
        return
   
    originalname = None
    for name in data:
        if (2 <= len(name) <= 3) and (name[1] == uniquename):
            originalname = name
            break
        elif (4 <= len(name) <= 5) and (name[2] == uniquename):
            originalname = name
            break

    print(originalname)

func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安


