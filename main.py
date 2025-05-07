import pandas as pd
from functions import verify_user, read_from_csv, register_new_user, find_user_ic, calculate_tax_relief

def page_one(filename):
    while True:
        print("\nMain Menu:")
        choice = input("1. Login\n2. Register\n3. Exit\nChoose an option: ").strip()
        
        if choice == '1':
            # 登录
            user_id = input("Enter your ID: ").strip()
            password = input("Enter your password (last 4 digits of your IC): ").strip()
            if verify_user(user_id, password) == True:
                second_page(user_id)  # 登录成功，跳转到第二页
                break  # 登录成功，跳转到第二页
            else:
                print("Login failed. Please try again.")
                    
        elif choice == '2':
            # 注册
            user_id = input("Enter your new ID: ").strip()
            ic_number = input("Enter your IC number (12 digits): ").strip()
            if ic_number.isdigit() and len(ic_number) == 12:
                if register_new_user(user_id,ic_number) == False:
                    None #if register failed, do nothing
                else:
                    second_page(user_id)  # 注册成功，跳转到第二页
                    break# register sucessful, automatically jump to second page
            else:
                print("Invalid IC number. Please enter a 12-digit number.") #if the ic number is not 12 digits, print out the error message

        elif choice == '3':
            # 退出
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
    
def second_page(user_id):
    filename = 'tax_data.csv'  # 数据存储文件名
    while True:
        print("\nSecond Page:")
        choice = input("1. View Tax Records\n2. Calculate Tax\n3. Logout\nChoose an option: ").strip()
        
        if choice == '1':
            # 查看税务记录
            df = read_from_csv(filename)
            if df is not None:
                df = df[df['UserID'] == user_id].reset_index(drop=True)
                df.index += 1
                print(df)  # 显示当前用户的税务记录
            else:
                print("No records found.")
                
        elif choice == '2':
            ic = find_user_ic(user_id) #根据用户ID查找IC号码
            calculate_tax_relief(user_id, ic)

        elif choice == '3':
            # 登出
            print("Logging out.")
            page_one(filename)  # 返回第一页
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def main():
    filename = 'tax_data.csv'  # 数据存储文件名
    print("Welcome to the Malaysian Tax Input Program")
    
    page_one(filename)


if __name__ == "__main__":
    main()
