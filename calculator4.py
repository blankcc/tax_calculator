#!/usr/bin/env python3
import sys
import csv
from multiprocessing import Process,Queue

q_userdata = Queue()
q_result = Queue()
class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
    def _get_path(self,parameter):
        try:
            index = self.args.index(parameter)
            return self.args[index+1]
        except:
            print("Parameter Error0")
            exit()
    @property
    def config_path(self):
        return self._get_path('-c')
    @property
    def userdata_path(self):
        return self._get_path('-d')
    @property
    def income_path(self):
        return self._get_path('-o')
args = Args()
class Config(object):
    def __init__(self):
        self.config = self._read_config()
    def _read_config(self):
        config = {}
        with open(args.config_path,'r') as f:
            for line in f.readlines():
                key,value = line.split('=')
                try:
                    config[key.strip()]=float(value.strip())
                except:
                    print("Parametr Error1")
                    exit()
        return config
    def _get_config(self,key):
        try:
            return self.config[key]
        except:
            print('Config Error')
            exit()
    @property
    def get_JiShuL(self):
        return self._get_config('JiShuL')
    @property
    def get_JiShuH(self):
        return self._get_config('JiShuH')
    @property
    def get_total_shebao(self):
        return (self._get_config('YangLao')+self._get_config('YiLiao')+
            self._get_config('ShiYe')+self._get_config('GongShang')+
            self._get_config('ShengYu')+self._get_config('GongJiJin'))

config = Config()
class UserData(Process):
    def __init__(self):
        self.userdata = self._read_users_data()
    def _read_users_data(self):
        userdata = []
        with open(args.userdata_path) as f:
            for line in f.readlines():
                EId,income = line.strip().split(',')
                try:
                    EId = int(EId)
                    income = int(income)
                except:
                    print("Parameter Error2")
                    exit()
                yield((EId,income))
    def run(self):
        for data in self._read_users_data():
            q_userdata.put(data)

class IncomeTaxCalculator(Process):
    def __init__(self,userdata):
        self.userdata = userdata
    def calc_society_insurance(self,income):
        if income<=config.get_JiShuL:
            return config.get_JiShuL*config.get_total_shebao
        elif config.get_JiShuL<income<config.get_JiShuH:
            return income * config.get_total_shebao
        else:
            return config.get_JiShuH*config.get_total_shebao
    def individual_income_tax(self,income):
        social_insurance_money = self.calc_society_insurance(income)
        real_income = income - social_insurance_money
        real_tax_due = real_income -3500
        if real_tax_due <= 0:
            return  '{:.2f}'.format(0),'{:.2f}'.format(real_income)
        elif real_tax_due <= 1500:
            return '{:.2f}'.format(real_tax_due*0.03),'{:.2f}'.format( income - real_tax_due*0.03 - social_insurance_money)
        elif 1500<real_tax_due<=4500:
            return '{:.2f}'.format(real_tax_due*0.1-105),'{:.2f}'.format(income - real_tax_due*0.1+105 - social_insurance_money)
        elif 4500<real_tax_due<=9000:
            return '{:.2f}'.format(real_tax_due*0.2-555),'{:.2f}'.format(income - real_tax_due*0.2+555 - social_insurance_money)
        elif 9000<real_tax_due<=35000:
            return '{:.2f}'.format(real_tax_due*0.25-1005),'{:.2f}'.format(income - real_tax_due*0.25+1005 - social_insurance_money)
        elif 35000<real_tax_due<=55000:
            return '{:.2f}'.format(real_tax_due*0.3-2755),'{:.2f}'.format(income - real_tax_due*0.3+2755 - social_insurance_money)
        elif 55000<real_tax_due<=80000:
            return '{:.2f}'.format(real_tax_due*0.35-5055),'{:.2f}'.format(income - real_tax_due*0.35+5055 - social_insurance_money)
        else:
            return '{:.2f}'.format(real_tax_due*0.45-13505),'{:.2f}'.format(income - real_tax_due*0.45+13505 - social_insurance_money)

    def calc_for_all_userdata(self):
        while True:
            try:
                EId, income = q_userdata.get(timeout=1)
            except queue.Empty:
                return
            data = [EId, income]
            social_insurance_money = '{:.2f}'.format(self.calc_society_insurance(income))
            tax, remain = self.individual_income_tax(income)
            data += [social_insurance_money, tax, remain]
            yield data

    def run(self):
        for data in self.calc_for_all_userdata():
            q_result.put(data)

class Exporter(Process):
    def run(self):
        with open(args.income_path, 'w', newline='') as f:
            while True:
                writer = csv.writer(f)
                try:
                    item = q_result.get(timeout=1)
                except queue.Empty:
                    return
                writer.writerow(item)

def main():
    Process(f1).start()
    Process(f2).start()
    Process(f3).start()
if __name__ == '__main__':
    workers = [
        UserData(),
        IncomeTaxCalculator(),
        Exporter()
    ]
    for worker in workers:
        worker.run()