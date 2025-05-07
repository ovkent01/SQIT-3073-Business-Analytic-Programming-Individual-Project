import pandas as pd
import os

filename = "tax_data.csv"
 # set  filename as global variable where is tax_data.csv  

def verify_user(user_id,password): 
    try:
        df = pd.read_csv(filename, dtype=str)  # use pandas to read the CSV file in string format
    except FileNotFoundError:
        print("No user data found. Please register first.")
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
        print(f"{user_id} registered successfully!")
        return True
    else:
        print("User ID already exists. Please choose a different ID and try again.")
        return False

def find_user_ic(user_id):
    """根据用户ID查找IC号码"""
    df = pd.read_csv(filename, dtype=str)  # read the CSV file in string format
    user_row = df[df["UserID"] == user_id]  # filter the dataframe to find the row with the given user_id
    if not user_row.empty:  # make sure the user exists
        ic = str(user_row.iloc[0]["IC"])# get the IC number of the user as string
        return ic # return the IC number
    
def calculate_tax(income, tax_relief):
    """根据收入和税收减免计算应缴税款"""
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
    """将数据保存到CSV文件"""
    df = pd.DataFrame([data])  # transform the data into a DataFrame
    try:
        df.to_csv(filename, mode='a', header=False, index=False)  # add the data to the CSV file
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")  # if there is an error, print out the error message

def read_from_csv(filename):
    """读取CSV文件中的数据并返回一个DataFrame"""
    try:
        return pd.read_csv(filename, dtype=str)  # read the CSV file in string format
    except FileNotFoundError:
        return None  # if the file does not exist, return None

def calculate_tax_relief(user_id, ic):
    tax_relief = 0

    # Step 1: annual income
    income = float(input("Please enter your annual income (RM): "))

    if income <= 9000:
        print("Your annual income is RM 9000 or less, you do not need to pay tax.")
        print("Tax payable: RM 0")
        return

    # 基本个人减免
    tax_relief += 9000

    # Step 2: 是否有配偶
    print("你是否有配偶？")
    print("1. 有")
    print("2. 没有")
    has_spouse = input("请选择（1或2）：").strip()
    if has_spouse == '1':
        spouse_income = float(input("请输入你配偶的年收入（RM）："))
        if spouse_income <= 4000:
            tax_relief += 4000

        # Step 3: 有几个孩子
        num_children = int(input("你有几个孩子？（最多可申报12人）："))
        if num_children > 12:
            num_children = 12
        tax_relief += num_children * 8000

    # Step 4: 是否有严重疾病
    print("你、你的配偶或孩子是否有严重疾病？")
    print("1. 有")
    print("2. 没有")
    has_serious_illness = input("请选择（1或2）：").strip()
    if has_serious_illness == '1':
        medical_expense = float(input("请输入医疗费用（最高 RM8,000）："))
        tax_relief += min(medical_expense, 8000)

    # Step 5: 生活用品支出
    lifestyle_expense = float(input("请输入你一年内的生活用品支出（书籍、运动、电脑、网络等，最高 RM2,500）："))
    tax_relief += min(lifestyle_expense, 2500)

    # Step 6: 教育费用
    education_expense = float(input("你是否有读大学或专业课程？请输入学费金额（最高 RM7,000）："))
    tax_relief += min(education_expense, 7000)

    # Step 7: 父母赡养
    print("你的父母还健在吗？")
    print("1. 是")
    print("2. 否")
    has_parents = input("请选择（1或2）：").strip()
    if has_parents == '1':
        father_age = int(input("你父亲的年龄是？"))
        mother_age = int(input("你母亲的年龄是？"))

        parental_relief = 0

        if father_age >= 60:
            father_income = float(input("你父亲的年收入是多少？"))
            if father_income <= 24000:
                parental_relief += 2500

        if mother_age >= 60:
            mother_income = float(input("你母亲的年收入是多少？"))
            if mother_income <= 24000:
                parental_relief += 2500

        tax_relief += parental_relief

    # 最后计算
    payable_tax = calculate_tax(income, tax_relief)
    
    print("\n----- 税务减免计算结果 -----")
    

    print(f"Annual income：RM {income:.2f}")
    print(f"Tax relief amount：RM {tax_relief:.2f}")
    print(f"Taxable income：RM {income-tax_relief:.2f}")
    print(f"Payable tax：RM {max(payable_tax,0):.2f}")
    if payable_tax <= 0:
        payable_tax = 0
        print("You do not need to pay tax. This calculation is only for reference. \n Please refer to the official government website for more details.")
    else:
        print("You need to pay tax. This calculation is only for reference.")
        print("For further details, please refer to the official government website.")
    print("--------------------------")
    
    data = {
        'UserID': user_id,
        'IC': ic,
        'Income': income,
        'Tax_Relief': tax_relief,
        'Tax_Payable': payable_tax
    }

    save_to_csv(data)