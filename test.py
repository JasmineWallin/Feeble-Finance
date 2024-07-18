from datetime import datetime, date
#lst = {'02/01/2023':'poop', '01/22/2023':'pee', '12/01/2022':'pooop', '12/02/2022':'something', '12/01/2019':'amungus'}
#sorted_dict = dict(sorted(lst.items(), key=lambda x: datetime.strptime(x, '%m/%d/%Y')))

'''
#lst = {'2/01/2023':1, '01/22/2023':2, '12/1/2022':3, '12/01/2019':'amungus'}
lst = {'2/2/2022': (0.01, '0/0/2020'), '1/27/2024': (50.0, '0/0/2020'), '6/30/2022': (80.0, '12/20/2023'), '2/17/2021': (300.07, '0/0/2020'), '7/25/2022': (20.25, '9/17/2023'), '1/3/2024': (250.22, '0/0/2020'), '12/1/2023': (500.0, '12/30/2024')}
sorted_dict = dict(sorted(lst.items(), key=lambda x: datetime.strptime(x[0], '%m/%d/%Y')))
#print(sorted_dict)

cool_list = ['poop', 'poo', 'hi', 'some']
for item in cool_list:
    if item == 'poop' or item == 'hi':
        continue
    print("im not poop or hi!", item)
'''
print(datetime.strptime('6/1/2024', '%m/%d/%Y') >= datetime.strptime(datetime.now().strftime('%m') + '/01/' + datetime.now().strftime('%Y'), '%m/%d/%Y'))