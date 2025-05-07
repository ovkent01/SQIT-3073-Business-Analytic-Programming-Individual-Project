import pandas as pd
from functions import verify_user, read_from_csv, register_new_user, find_user_ic, calculate_tax_relief

def page_one(filename):
    while True:
        print("\nMain Menu:")
        choice = input("1. Login\n2. Register\n3. Exit\nChoose an option: ").strip()
        
        if choice == '1':
            # login
            user_id = input("Enter your ID: ").strip()
            password = input("Enter your password (last 4 digits of your IC): ").strip()
            if verify_user(user_id, password) == True:
                second_page(user_id)  # login successful, jump to second page
                break
            else:
                print("Login failed. Please try again.")
                    
        elif choice == '2':
            # register
            user_id = input("Enter your new ID: ").strip()
            ic_number = input("Enter your IC number (12 digits): ").strip()
            if ic_number.isdigit() and len(ic_number) == 12:
                if register_new_user(user_id,ic_number) == False:
                    None #if register failed, do nothing
                else:
                    second_page(user_id)  
                    break # register sucessful, automatically jump to second page
            else:
                print("Invalid IC number. Please enter a 12-digit number.") #if the ic number is not 12 digits, print out the error message

        elif choice == '3':
            # exit
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
    
def second_page(user_id):
    filename = 'tax_data.csv'  # file name for tax data
    while True:
        print("\nSecond Page:")
        choice = input("1. View Tax Records\n2. Calculate Tax\n3. Logout\nChoose an option: ").strip()
        
        if choice == '1':
            # check tax records
            df = read_from_csv(filename)
            if df is not None:
                df = df[df['UserID'] == user_id].reset_index(drop=True)  
                # filter the dataframe to find the row with the given user_id
                df.index += 1
                print("\n Your Tax Records:")
                print(df)  # show the tax records of the user
            else:
                print("No records found.")
                
        elif choice == '2':
            ic = find_user_ic(user_id) #according to the user ID, find the IC number of the user
            calculate_tax_relief(user_id, ic)

        elif choice == '3':
            # logout
            print("Logging out.")
            page_one(filename)  # back to the first page
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def main():
    filename = 'tax_data.csv'  # file name for tax data
    print("\n\nWelcome to the Malaysian Tax Input Program")
    
    page_one(filename)


if __name__ == "__main__":
    main()
