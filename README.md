# Individual Assignment
This is an university assignment project, for study use only
here is the requirements.
- https://docs.google.com/document/d/1aSi6CoTi-UpV1AO7xDDxB3wQGKGKYUfHO7KjlX4gW4Y/edit?tab=t.0
- SQIT 3073: Business Analytic Programming Individual Project -  10% Marks
bellow is a short introduction

# Malaysian Personal Income Tax Calculator (Console Application)

## Overview

This project is a simple **console-based application** designed to help Malaysian taxpayers:
- **Register and log in** to a secure profile
- **Calculate their personal income tax reliefs**
- **Store and view their tax records**

It is designed as part of an educational project and serves as a practical demonstration of user authentication, data processing, and basic tax computations using Python.

---

## Features

- 🔐 User registration and login (based on IC number verification)
- 📊 Tax calculation based on Malaysia's tax relief categories
- 📁 Automatic storage of tax calculation records in a `.csv` file
- 👤 Each user can only access **their own records**

---

## Technologies Used

- Python 3.x
- pandas (for data manipulation and CSV operations)

---

## How to Run

### 1. Clone this repository or download the files manually:

```bash
git clone https://github.com/your-username/tax-calculator.git
cd tax-calculator
```
### 2. Install dependencies (if not already installed):
```bash
pip install pandas
```
### 3. Run the program:
```bash
python main.py
```

## File Structure
- main.py – Main program logic and user interface
- functions.py – Functions for authentication, tax calculation, and CSV handling
- tax_data.csv – Data file storing user tax records (automatically generated)

## Example Workflow
1. Start the Program
  You'll see a menu to Login, Register, or Exit.
2. Register a New User
  Provide a user ID and a valid 12-digit IC number.
3.Login
  Use your user ID and the last 4 digits of your IC as your password.
4. After Logging In
  Choose to:
  - View your personal tax calculation history
  - Calculate new tax based on your personal details
  - Logout

## Notes
- The program ensures that users can only access their own data.
- IC and user ID are used to identify and authenticate each individual user.
- Data is saved in a simple tax_data.csv file and persists between sessions.

## Author
- Vincent Ooi Jing Kent
\nUndergraduate Student Project
- For academic use only.


