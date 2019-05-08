#Author: Bryan Bijonowski
#Date Created: 05/01/2019
#Date Modified: 05/02/2019
#Purpose: To provide information regarding amount owed for taxes based on total tax liability.

#TO-DO:
#See Below
#Add deduction features (standardized and itemized)
#Add restart feature upon user input error
#Add color text


filing_status = str(input("Welcome. Please designate your filing status as follows:\n\n"
      "Single = S\n"
      "Head of Household = H\n"
      "Married Filing Jointly = M\n"
      "Married Filing Separately = T\n"
      "Input Tax Brackets Manually = A\n\n"
      "Filing Status: "))

if filing_status.upper() == "S":
    
    tax_a = float(9525.0)
    tax_b = float(38700.0)
    tax_c = float(82500.0)
    tax_d = float(157500.0)
    tax_e = float(200000.0)
    tax_f = float(500000.0)
    
elif filing_status.upper() == "H":
    
    tax_a = float(13600.0)
    tax_b = float(51800.0)
    tax_c = float(82500.0)
    tax_d = float(157500.0)
    tax_e = float(200000.0)
    tax_f = float(500000.0)
    
elif filing_status.upper() == "M":
    
    tax_a = float(19050.0)
    tax_b = float(77400.0)
    tax_c = float(165000.0)
    tax_d = float(315000.0)
    tax_e = float(400000.0)
    tax_f = float(600000.0)
    
elif filing_status.upper() == "T":
    
    tax_a = float(9525.0)
    tax_b = float(38700.0)
    tax_c = float(82500.0)
    tax_d = float(157000.0)
    tax_e = float(200000.0)    
    tax_f = float(300000.0)

elif filing_status.upper() == "A":
    
    try:
        
        tax_a = float(input('What is the maximum income at 10% tax rate for your filing status?: '))
        tax_b = float(input('What is the maximum income at 12% tax rate for your filing status?: '))
        tax_c = float(input('What is the maximum income at 22% tax rate for your filing status?: '))
        tax_d = float(input('What is the maximum income at 24% tax rate for your filing status?: '))
        tax_e = float(input('What is the maximum income at 32% tax rate for your filing status?: '))
        tax_f = float(input('What is the maximum income at 35% tax rate for your filing status?: ')) 
        
    except ValueError:
        
        print("All values supplied must be a whole or decimal number. Exiting...")
        exit()
    

else:
    
    print("You did not select an appropriate filing status. Exiting...")
    exit()


try:
    
    months_worked = int(input("How many months in the current tax year have you worked?: "))
    if months_worked > 12:
        print("That is too many months in a calendar year. Exiting...")
        exit()
        
    paychecks = int(input("How many paychecks do you receive in one year?: "))
    witholding = float(input("How much Federal Taxes are being withheld each paycheck?: "))
    income = float(input("What is your yearly gross income?: ")) 
    
    
except ValueError:
    
    print("All values supplied must be a whole or decimal number. Exiting...")
    exit()
    
paychecks_received = ((paychecks / 12) * months_worked)
months_not_worked = (12 - months_worked)
gross_income = income

if months_worked < 12:
    income = round(((income / paychecks) * paychecks_received), 2)


def tax_check_a(income, tax_liability=0):
    """Checks to see if income is greater than the first tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income > tax_a):
        tax_liability += (tax_a * .10)
        total_tax_liability = tax_check_b(income, tax_liability)
        return total_tax_liability
         
    else:
        tax_liability += (income * .10)
        return tax_liability
            
        
def tax_check_b(income, tax_liability):
    """Checks to see if income is greater than the second tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income > tax_b):
        tax_liability += ((tax_b - tax_a) * .12)
        tax_check_c(income, tax_liability)
        total_tax_liability = tax_check_c(income, tax_liability)
        return total_tax_liability
    
    else:
        tax_liability += ((income - tax_a) * .12)
        return tax_liability
        
def tax_check_c(income, tax_liability):
    """Checks to see if income is greater than the third tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income > tax_c):
        tax_liability += ((tax_c - tax_b) * .22)
        tax_check_d(income, tax_liability)
        total_tax_liability = tax_check_d(income, tax_liability)
        return total_tax_liability        
        
    else:
        tax_liability += ((income - tax_b) * .22)
        return tax_liability
        
def tax_check_d(income, tax_liability):
    """Checks to see if income is greater than the fourth tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income > tax_d):
        tax_liability += ((tax_d - tax_c) * .24)
        tax_check_e(income, tax_liability)
        total_tax_liability = tax_check_e(income, tax_liability)
        return total_tax_liability       
        
    else:
        tax_liability += ((income - tax_c) * .24)
        return tax_liability

def tax_check_e(income, tax_liability):
    """Checks to see if income is greater than the fifth tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income > tax_e):
        tax_liability += ((tax_e - tax_d) * .32)
        tax_check_f(income, tax_liability)
        total_tax_liability = tax_check_f(income, tax_liability)
        return total_tax_liability        
        
    else:
        tax_liability += ((income - tax_e) * .32)
        return tax_liability
        
def tax_check_f(income, tax_liability):
    """Checks to see if income is less than or equal to, the sixth tax bracket, or if it is in the seventh tax bracket. Adds maximum liability to total liability if income is above threshold"""
    
    if (income <= tax_f):
        tax_liability += ((tax_f - tax_e) * .35)
        return tax_liability
    else:
        tax_liability += (((tax_f - tax_e) * .35) + ((income - tax_f) * .37))
        return tax_liability
        
  
total_tax_liability = round(tax_check_a(income), 2)
total_witholding = round((witholding * paychecks_received), 2)
net_income = round((income - total_tax_liability), 2)
tax_withold = (tax_check_a(gross_income)) / paychecks
tax_withold = round(tax_withold, 2)
difference = round((witholding - tax_withold), 2)
abs_difference = abs(difference)


print("\nTotal Gross Income YTD: ${income}.".format(income=income)) 
#Gross Income earned based on number of months worked in the taxable calendar year, as specified by the user.

print('\nTotal Tax Liability YTD: ${total_tax_liability}.'.format(total_tax_liability=total_tax_liability))
#Total Tax Liability determined against income as specified by the user.

print("\nTotal Net Income YTD: ${net_income}.".format(net_income=net_income))
#Net income earned based on Total Gross Income YTD - Total Tax Liability YTD.

print("\nTotal Witheld YTD: ${total_witholding}.".format(total_witholding=total_witholding))
#Total Witheld based on witheld amount, as specified by user, multiplied by paychecks received.

print("\nTotal Witheld Per Paycheck: ${witholding}."
"\n\nCorrect Total To Be Witheld Per Paycheck: ${tax_withold}.".format(witholding=witholding, 
                                                                    tax_withold=tax_withold))
#Specifies both current witheld amount, specified by user, and the amount that should have been witheld per paycheck throughout the taxable calendar year.

if difference < 0:
    print("\nTotal Deficiency Per Paycheck: ${abs_difference}. ".format(abs_difference=abs_difference))
else:
    print("\nTotal Overage Per Paycheck: ${abs_difference}.".format(abs_difference=abs_difference))
#Checks to see the difference between what was witheld per paycheck, and what should have been witheld per paycheck, and then informs the user one way or the other.



if total_tax_liability > total_witholding:
    diff1 = round((total_tax_liability - total_witholding), 2)
    
    try:
        paycheck_divide = round((diff1 / months_not_worked), 2)
        print("\nTotal Owed To The Federal Government: ${diff1}.\n\nYou should withold an additional ${paycheck_divide} per paycheck for the remaining {months_not_worked} months.".format(diff1=diff1, 
                                                                                                                                                                                         paycheck_divide=paycheck_divide, months_not_worked=months_not_worked))
    except:
        paycheck_divide = round((diff1 / 1), 2)
        print("\nTotal Owed To The Federal Government: ${diff1}.".format(diff1=diff1))       
        
else:
    diff2 = abs(round((total_tax_liability - total_witholding), 2))
    print("\nTotal Estimated Federal Government Refund: ${diff2}.".format(diff2=diff2))






#Fix Below:

"""Welcome. Please designate your filing status as follows:
Single = S
Head of Household = H
Married Filing Jointly = M
Married Filing Separately = T
Filing Status: s
How much Federal Taxes are being withheld each paycheck?: 1012.3
How many paychecks do you receive in one year?: 12
How many months in the current tax year have you worked?: 8
What is your yearly gross income?: 74450
Total Gross Income YTD: $49633.33.
Total Tax Liability YTD: $6858.83.
Total Net Income YTD: $42774.5.
Total Witheld YTD: $8098.4.
Total Witheld Per Paycheck: $1012.3.
Correct Total To Be Witheld Per Paycheck: $1026.54.
Total Deficiency Per Paycheck: $14.24. 
Total Estimated Federal Government Refund: $1239.57."""    