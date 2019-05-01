
#Author: Bryan Bijonowski
#Date Created: 05/01/2019
#Date Modified: 05/01/2019
#Purpose: To provide information regarding amount owed for taxes based on total tax liability.

print("Please answer the following questions according to your filing status...\n")

try:
    
    tax_a = float(input('What is the maximum income at 10% tax rate for your filing status?: '))
    tax_b = float(input('What is the maximum income at 12% tax rate for your filing status?: '))
    tax_c = float(input('What is the maximum income at 22% tax rate for your filing status?: '))
    tax_d = float(input('What is the maximum income at 24% tax rate for your filing status?: '))
    tax_e = float(input('What is the maximum income at 32% tax rate for your filing status?: '))
    tax_f = float(input('What is the maximum income at 35% tax rate for your filing status?: '))
    witholding = float(input("How much Federal Taxes are being withheld each paycheck?: "))
    paychecks = int(input("How many paychecks do you receive in one year?: "))
    months_worked = int(input("How many months in the current tax year have you worked?: "))
    income = float(input("What is your yearly gross income?: ")) 
    
    
except ValueError:
    print("All values supplied must be a whole or decimal number. Exiting...")
    exit()
    
paychecks_received = ((paychecks / 12) * months_worked)

if months_worked < 12:
    if paychecks == 26:
        income = ((income / paychecks) * paychecks_received)
    elif paychecks == 24:
        income = ((income / paychecks) * paychecks_received)
    elif paychecks == 12:
        income = ((income / paychecks) * paychecks_received)
    else:
        print("Sorry, that is not a valid number of paychecks")
        exit()


def tax_check_a(income, tax_liability=0):
    """Checks to see if income is greater than first tax bracket of $9,525"""
    
    if (income > tax_a):
        tax_liability += (tax_a * .10)
        cost = tax_check_b(income, tax_liability)
        return cost
        
        
    else:
        tax_liability += (income * .10)
        return tax_liability
            
        
def tax_check_b(income, tax_liability):
    """Checks to see if income is greater than second tax bracket of $38,700"""
    
    if (income > tax_b):
        tax_liability += ((tax_b - tax_a) * .12)
        tax_check_c(income, tax_liability)
        cost = tax_check_c(income, tax_liability)
        return cost
    
    else:
        tax_liability += ((income - tax_a) * .12)
        return tax_liability
        
def tax_check_c(income, tax_liability):
    """Checks to see if income is greater than third tax bracket of $82,500"""
    
    if (income > tax_c):
        tax_liability += ((tax_c - tax_b) * .22)
        tax_check_d(income, tax_liability)
        cost = tax_check_d(income, tax_liability)
        return cost        
        
    else:
        tax_liability += ((income - tax_b) * .22)
        return tax_liability
        
def tax_check_d(income, tax_liability):
    """Checks to see if income is greater than fourth tax bracket of $157,500"""
    
    if (income > tax_d):
        tax_liability += ((tax_d - tax_c) * .24)
        tax_check_e(income, tax_liability)
        cost = tax_check_e(income, tax_liability)
        return cost        
        
    else:
        tax_liability += ((income - tax_c) * .24)
        return tax_liability

def tax_check_e(income, tax_liability):
    """Checks to see if income greater than fifth tax bracket of $200,000"""
    
    if (income > tax_e):
        tax_liability += ((tax_e - tax_d) * .32)
        tax_check_f(income, tax_liability)
        cost = tax_check_f(income, tax_liability)
        return cost        
        
    else:
        tax_liability += ((income - tax_e) * .32)
        return tax_liability
        
def tax_check_f(income, tax_liability):
    """Checks to see if income is less than, equal to, or greater than the sixth tax bracket of $500,000"""
    
    if (income <= tax_f):
        tax_liability += ((tax_f - tax_e) * .35)
        return tax_liability
    else:
        tax_liability += (((tax_f - tax_e) * .35) + ((income - tax_f) * .37))
        return tax_liability
        
  
cost = tax_check_a(income)
total_witholding = (witholding * paychecks_received)

print("Your total taxable income is {income}".format(income=income))
print('\nYour yearly tax liability is ${cost}'.format(cost=cost))
print("\nYour total witholding is ${total_witholding}".format(total_witholding=total_witholding))

if cost > total_witholding:
    diff1 = (cost - total_witholding)
    paycheck_divide = (diff1 / paychecks)
    print("\nYou will owe the Federal Government ${diff1}.\n\nYou should withold an additional ${paycheck_divide} per paycheck".format(diff1=diff1, 
                                                                                                                                       paycheck_divide=paycheck_divide))
else:
    diff2 = abs(cost - total_witholding)
    print("\nThe Federal Government will issue an estimated refund in the amount of ${diff2}".format(diff2=diff2))
    


        


        

    



    