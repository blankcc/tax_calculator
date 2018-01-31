#!/usr/bin/env python3
import sys
try:
    int(sys.argv[1])
except:
    print("Parameter Error")
    exit()
salary = int(sys.argv[1])
tax_due = salary - 3500
if tax_due <= 0:
    print('0.00')
elif tax_due <= 1500:
    print(format(tax_due*0.03,".2f"))
elif 1500<tax_due<=4500:
    print(format(tax_due*0.1-105,".2f"))
elif 4500<tax_due<=9000:
    print(format(tax_due*0.2-555,".2f"))
elif 9000<tax_due<=35000:
    print(format(tax_due*0.25-1005,".2f"))
elif 35000<tax_due<=55000:
    print(format(tax_due*0.3-2755,".2f"))
elif 55000<tax_due<=80000:
    print(format(tax_due*0.35-5505,".2f"))
else:
    print(format(tax_due*0.45-13505,".2f"))
