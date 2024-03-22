# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:02:20 2020

@author: m.ryabko
"""

from datetime import date
a = date(2020,7,28)
b = date(2023,4,25)

#date.timedelta(7)
delta=(b-a).days
kupon=110.96
p=13.5
pb=4.25

po = p-pb-5

res_kupon=0.65*po*kupon/p +0.87*(kupon-po*kupon/p)
r_kupon = 0.65*po*kupon/p +1*(kupon-po*kupon/p)
res=366*(-245.97+5*r_kupon+res_kupon*28)/delta/10245.97

2116.01
12.33
313