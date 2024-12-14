#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2024/12/13 20:47
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""
"""

from netCDF4 import Dataset
from .. import Ttime
import numpy as np
from datetime import datetime, timedelta


def f_load_time(fin, fmethod='time'):

    ncid = Dataset(fin, 'r')

    if fmethod == 'Times' and 'Times' in ncid.variables.keys():
        Times_fvcom = ncid.variables['Times'][:]
        TIME = np.apply_along_axis(lambda row: b''.join(row).decode(), 1, Times_fvcom.data).tolist()
        Times = [datetime.fromisoformat(TIME[i]) for i in range(len(TIME))]
    else:
        Itime = ncid.variables['Itime'][:]
        Itime2 = ncid.variables['Itime2'][:]
        time = Itime + Itime2 / 1000 / 3600 / 24  # --> day
        if 'format' in ncid.variables['Itime'].ncattrs() and 'MJD' in ncid.variables['Itime'].format:
            Times = [datetime(1858, 11, 17) + timedelta(days=x) for x in time]
        else:
            return None
    Ttimes = Ttime(Times=Times)
    return Ttimes

