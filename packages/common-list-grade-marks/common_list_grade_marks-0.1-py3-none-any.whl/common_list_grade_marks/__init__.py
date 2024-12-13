def common_elements(list1,list2):
    common_list =[]
    i=0
    while i < len(list1):
        if list1[i] in list2:
            common_list.append(list1[i])
        i=i+1
    print(common_list)


#common_elements([1,2,3],[1,2,4])
name = "saral kumar"
#print(name)

def marks_function(marks):
    if marks >=91 and marks<=100:
        print("A+")

    elif marks >=81 and marks <=90:
        print("A")

    elif marks >= 71 and marks <=80: #77>71 and 77<=80
        print("B")

    elif marks >= 61 and marks <= 70:
        print("C")

    elif marks >= 51 and marks <= 60:
        print("D")

    elif marks >=36 and marks <=50:
        print("E")

    elif marks >=0 and marks<=35:
        print("fail")
    else:
        print("invalid marks")


#marks_function(57)

