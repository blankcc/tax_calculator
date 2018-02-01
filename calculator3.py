#!/usr/bin/env python3
import sys
import csv

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
    def _get_path(self,parameter):
        if self.args.index(parameter):
            index = self.args.index(parameter)
            return self.args[index+1]
        else:
            raise ParameterError()
    @property
    def config_path(self):
        return self._get_path(self,'-c')
    @property
    def userdata_path(self):
        return self._get_path(self,'-d')
    @property
    def income_path(delf):
        return self._get_path(self,'-o')

args = Args()
class Config(object):
    def __init__(self):
        self.config = self._read_config()
    def _read_config(self):
        config = {}
        with open(args.config_path,'r') as f:
            for line in f.readlines():
                key,value = line.split('=')
                if float(value.strip()):
                    config[key.strip()]=float(value.strip())
                else:
                    raise ParameterError()
        return config
    def get_config(self,key):
        return self.config[key]
    @property
    def get_JiShuL(self):
        return self.config[JiShuL]
    @property
    def get_JiShuH(self):
        return self.config[JiShuH]
    @property
    def get_total_shebao(self):
        return (self.config[YangLao]+self.config[YiLiao]+
            self.config[ShiYe]+self.config[GongShang]+
            self.config[ShengYu]+self.config[GongJiJin])

class UserData(object):
    def __init__(self):
        self.userdata = self._read_users_data()
    def _read_users_data(self):
        userdata = []
        with open(args.userdata_path,'r') as f:
            for line in f.readlines():
                EId,income = line.strip().split(',')
            try:
                EId = int(EId)
                income = int(income)
            except:
                print("Parameter Error")
                exit()
            userdata.append(EId,income)
        return userdata
    def __iter__(self):
        return iter(self.userdata)

class IncomeTaxCalculator(object):
    def calc_for_all_userdata(self):
    def calc_society_insurance(self):
    def export(self,default='csv'):
        result = self.calc_for_all_userdata()
        with open("") as f:
            write = csv.writer(f)
            writer.writerows(result)
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
