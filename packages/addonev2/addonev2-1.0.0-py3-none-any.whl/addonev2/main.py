def add_one():
    try:
        user_input = input("请输入一个数字: ")
        number = int(user_input)
        print(f"输出结果: {number + 1}")
    except ValueError:
        print("输入无效，请输入一个数字！")
def multiply_two():
    try:
        user_input = input("请输入一个数字: ")
        number = int(user_input)
        print(f"输出结果: {number * 2}")
    except ValueError:
        print("输入无效，请输入一个数字！")
def minus_one():
    try:
        user_input = input("请输入一个数字: ")
        number = int(user_input)
        print(f"输出结果: {number - 1}")
    except ValueError:
        print("输入无效，请输入一个数字！")
if __name__ =="__main__":
    add_one()
    multiply_two()
    minus_one()
