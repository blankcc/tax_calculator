#!/usr/bin/env python3
import sys

def cal(nos,salaries):
    for salary in salaries:
        social_security = salary*0.165
        tax_due = salary - social_security - 3500
        if tax_due <= 0:
            final_salaries.append(salary - social_security)
        elif tax_due <= 1500:
            final_salaries.append(salary - tax_due*0.03 - social_security)
        elif 1500<tax_due<=4500:
            final_salaries.append(salary - tax_due*0.1+105 - social_security)
        elif 4500<tax_due<=9000:
            final_salaries.append(salary - tax_due*0.2+555 - social_security)
        elif 9000<tax_due<=35000:
            final_salaries.append(salary - tax_due*0.25+1005 - social_security)
        elif 35000<tax_due<=55000:
            final_salaries.append(salary - tax_due*0.3+2755 - social_security)
        elif 55000<tax_due<=80000:
            final_salaries.append(salary - tax_due*0.35+5055 - social_security)
        else:
            final_salaries.append(salary - tax_due*0.45+13505 - social_security)
    for no in range(len(nos)):
        print("{}:{:.2f}".format(nos[no],final_salaries[no]))

nos = []
salaries = []
final_salaries = []
try:
    for arg in sys.argv[1:]:
        temp = arg.split(":")
        nos.append(int(temp[0]))
        salaries.append(int(temp[1]))
except:
    print("Parameter Error")
    exit()
cal(nos,salaries)
