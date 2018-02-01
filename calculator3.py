#!/usr/bin/env python3
import sys
import csv
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
    def _get_path(self,parameter):
        try:
            index = self.args.index(parameter)
            return self.args[index+1]
        except:
            print("Parameter Error")
            exit()
    @property
    def config_path(self):
        return self._get_path(self,'-c')
    @property
    def userdata_path(self):
        return self._get_path(self,'-d')
    @property
    def income_path(self):
        return self._get_path(self,'-o')

class Config(object):
    def __init__(self):
        self.config = self._read_config()
    def _read_config(self):
        config = {}
        with open(Args.config_path,'r') as f:
            for line in f.readlines():
                key,value = line.split('=')
                try:
                    config[key.strip()]=float(value.strip())
                except:
                    print("Parametr Error")
                    exit()
        return config
    def get_config(self,key):
        return self.config[key]
    @property
    def get_JiShuL(self):
        return self.config['JiShuL']
    @property
    def get_JiShuH(self):
        return self.config['JiShuH']
    @property
    def get_total_shebao(self):
        return (self.config['YangLao']+self.config['YiLiao']+
            self.config['ShiYe']+self.config['GongShang']+
            self.config['ShengYu']+self.config['GongJiJin'])

class UserData(object):
    def __init__(self):
        self.userdata = self._read_users_data()
    def _read_users_data(self):
        userdata = []
        with open(Args.userdata_path,'r') as f:
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
        result = []
        for employee_id, income in self.userdata:
            data = [employee_id, income]
            social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
            tax, remain = self.calc_income_tax_and_remain(income)
            data += [social_insurance_money, tax, remain]
            result.append(data)
        return result
    def calc_society_insurance(income):
        if income<=Config.get_JiShuL:
            return Config.get_JiShuL*Config.get_total_shebao
        elif Config.get_JiShuL<income<Config.get_JiShuH:
            return income * Config.get_total_shebao
        else:
            return Config.get_JiShuH*Config.get_total_shebao
    def individual_income_tax(self,income):
        social_insurance_money = self.calc_society_insurance(income)
        real_income = income - social_insurance_money
        if real_income <= 0:
            return  '{:.2f}'.format(0),'{:.2f}'.format(real_income)
        elif real_income <= 1500:
            return '{:.2f}'.format(real_income*0.03),'{:.2f}'.format( income - real_income*0.03 - social_insurance_money)
        elif 1500<real_income<=4500:
            return '{:.2f}'.format(real_income*0.1-105),'{:.2f}'.format(income - real_income*0.1+105 - social_insurance_money)
        elif 4500<real_income<=9000:
            return '{:.2f}'.format(real_income*0.2-555),'{:.2f}'.format(income - real_income*0.2+555 - social_insurance_money)
        elif 9000<real_income<=35000:
            return '{:.2f}'.format(real_income*0.25-1005),'{:.2f}'.format(income - real_income*0.25+1005 - social_insurance_money)
        elif 35000<real_income<=55000:
            return '{:.2f}'.format(real_income*0.3-2755),'{:.2f}'.format(income - real_income*0.3+2755 - social_insurance_money)
        elif 55000<real_income<=80000:
            return '{:.2f}'.format(real_income*0.35-5055),'{:.2f}'.format(income - real_income*0.35+5055 - social_insurance_money)
        else:
            return '{:.2f}'.format(real_income*0.45-13505),'{:.2f}'.format(income - real_income*0.45+13505 - social_insurance_money)

    def export(self,default='csv'):
        result = self.calc_for_all_userdata()
        with open(Args.userdata_path,'w') as f:
            write = csv.writer(f)
            writer.writerows(result)

if __name__ = '__main__':

