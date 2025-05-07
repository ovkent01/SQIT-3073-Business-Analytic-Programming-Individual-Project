import pandas as pd
import os

filename = "tax_data.csv"
 # set  filename as global variable where is tax_data.csv  

def verify_user(user_id,password): 
    try:
        df = pd.read_csv(filename, dtype=str)  # use pandas to read the CSV file in string format
    except FileNotFoundError:
        print("\nNo user data found. Please register first.")
        return False
    # try whether the file exists, if not, print out the error message and return false
    
    user_row = df[df["UserID"] == user_id]  # filter the dataframe to find the row with the given user_id
    if not user_row.empty:  # make sure the user exists
        ic = user_row.iloc[0]["IC"]  # get the IC number of the user
        ic = str(ic) # convert the IC number to string
        last4 = ic[-4:]              # get the last 4 digits of the IC number
        if last4 == password:
            print("\nlogin success!")
            return True
        else:
            print("\nPassword does NOT match ❌, please try again.")
            return False
    else:
            print("\nUser not found, please try again.")
            return False
    
def register_new_user(user_id, ic_number):
    # register a new user
    try:
        df = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['UserID', 'IC', 'Income', 'Tax_Relief', 'Tax_Payable'])
    # if the file does not exist, create a new dataframe with the specified columns

    if df[df["UserID"] == user_id].empty:
        new_user = pd.DataFrame({
            'UserID': [user_id],
            'IC': [ic_number],
            'Income': [0], # Initialize row for new user is only registered, no input income yet
            'Tax_Relief': [0],
            'Tax_Payable': [0]
        })

        file_exists = os.path.exists(filename)
        is_empty = not file_exists or os.path.getsize(filename) == 0

        new_user.to_csv(filename, mode='a', header=is_empty, index=False)
        print(f"\n{user_id} registered successfully!")
        return True
    else:
        print("\nUser ID already exists. Please choose a different ID and try again.")
        return False

def find_user_ic(user_id):
    """according to the user ID, find the IC number of the user"""
    df = pd.read_csv(filename, dtype=str)  # read the CSV file in string format
    user_row = df[df["UserID"] == user_id]  # filter the dataframe to find the row with the given user_id
    if not user_row.empty:  # make sure the user exists
        ic = str(user_row.iloc[0]["IC"])# get the IC number of the user as string
        return ic # return the IC number
    
def calculate_tax(income, tax_relief):
    """according to the income and tax relief, calculate the tax amount"""
    taxable_income = income - tax_relief  # calculate taxable income

    # calculate tax based on taxable income
    if taxable_income <= 50000:
        tax = taxable_income * 0.01  # 1% tax rate for income up to RM50,000
    elif taxable_income <= 100000:
        tax = 50000 * 0.01 + (taxable_income - 50000) * 0.03  # income from RM50,000 to RM100,000, tax rate is 3%
    elif taxable_income <= 250000:
        tax = 50000 * 0.01 + 50000 * 0.03 + (taxable_income - 100000) * 0.08  # income from RM100,000 to RM250,000, tax rate is 8%
    elif taxable_income <= 500000:
        tax = 50000 * 0.01 + 50000 * 0.03 + 150000 * 0.08 + (taxable_income - 250000) * 0.14  # income from RM250,000 to RM500,000, tax rate is 14%
    else:
        tax = 50000 * 0.01 + 50000 * 0.03 + 150000 * 0.08 + 250000 * 0.14 + (taxable_income - 500000) * 0.24  # income above RM500,000, tax rate is 24%
    
    return tax #return the tax amount

def save_to_csv(data):
    """save the data to a CSV file"""
    df = pd.DataFrame([data])  # transform the data into a DataFrame
    try:
        df.to_csv(filename, mode='a', header=False, index=False)  # add the data to the CSV file
        print("\nData saved successfully!")
    except Exception as e:
        print(f"\nError saving data: {e}")  # if there is an error, print out the error message

def read_from_csv(filename):
    """read the data from a CSV file and return it as a DataFrame"""
    try:
        return pd.read_csv(filename, dtype=str)  # read the CSV file in string format
    except FileNotFoundError:
        return None  # if the file does not exist, return None

def calculate_tax_relief(user_id, ic):
    tax_relief = 0

    # Step 1: annual income
    income = float(input("\nPlease enter your annual income (RM): "))

    if income <= 9000:
        print("Your annual income is RM 9000 or less, you do not need to pay tax.")
        print("Tax payable: RM 0")
        return

    # basic tax relief
    tax_relief += 9000

    # Step 2: ask if the user has a spouse
    print("\nAre you married?")
    print("1. Yes")
    print("2. No")
    has_spouse = input("Please select (1 or 2): ").strip()
    if has_spouse == '1':
        spouse_income = float(input("\nPlease enter your spouse's income per year (RM): "))
        if spouse_income <= 4000:
            tax_relief += 4000

        # Step 3: how many children
        num_children = int(input("\nHow many children do you have? (maximum can be up to 12): "))
        if num_children > 12:
            num_children = 12
        tax_relief += num_children * 8000

    # Step 4: serious illness 
    print("\nDo you, your spouse, or your children have any serious illness?")
    print("1. Yes")
    print("2. No")
    has_serious_illness = input("Please select (1 or 2): ").strip()
    if has_serious_illness == '1':
        medical_expense = float(input("\nPlease enter your medical expenses (maximum relief RM8,000): "))
        tax_relief += min(medical_expense, 8000)

    # Step 5: Lifestyle expenses
    lifestyle_expense = float(input("\nPlease enter your lifestyle expenses (Books, Sports, Computer, Internet, etc., maximum RM2,500): ")) 
    tax_relief += min(lifestyle_expense, 2500)

    # Step 6: education expenses
    education_expense = float(input("\nPlease enter your education expenses (maximum RM7,000): "))
    tax_relief += min(education_expense, 7000)

    # Step 7: Parental relief
    print("\nDo your parents still are alive?")
    print("1. Yes")
    print("2. No")
    has_parents = input("Please select (1 or 2): ").strip()
    if has_parents == '1':
        father_age = int(input("\nPlease enter your father's age: "))
        mother_age = int(input("Please enter your mother's age: "))

        parental_relief = 0

        if father_age >= 60:
            father_income = float(input("\nPlease enter your father's annual income (RM): "))
            if father_income <= 24000:
                parental_relief += 2500

        if mother_age >= 60:
            mother_income = float(input("Please enter your mother's annual income (RM): "))
            if mother_income <= 24000:
                parental_relief += 2500

        tax_relief += parental_relief

    # Final Calculation
    payable_tax = calculate_tax(income, tax_relief)
    
    print("\n\n----- Tax Calculation Result -----")
    print(f"Annual income：RM {income:.2f}")
    print(f"Tax relief amount：RM {tax_relief:.2f}")
    print(f"Taxable income：RM {income-tax_relief:.2f}")
    print(f"Payable tax：RM {max(payable_tax,0):.2f}")
    print("----------------------------------")
    if payable_tax <= 0:
        payable_tax = 0
        print("\nYou do not need to pay tax. This calculation is only for reference.\nPlease refer to the official government website for more details.")
    else:
        print("\nYou need to pay tax. This calculation is only for reference.")
        print("For further details, please refer to the official government website.")
    print("-----------------------------------")
    
    data = {
        'UserID': user_id,
        'IC': ic,
        'Income': income,
        'Tax_Relief': tax_relief,
        'Tax_Payable': payable_tax
    }

    save_to_csv(data)
    print("\nScroll up a bit to see your tax records.")