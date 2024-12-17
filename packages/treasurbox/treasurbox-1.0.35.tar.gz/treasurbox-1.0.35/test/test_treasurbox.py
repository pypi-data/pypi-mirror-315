#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-17 17:52:59
# @Author: Alan
# @File: test_treasurbox.py
# @Describe: test treasurbox

import treasurbox
from treasurbox.src.work_faker import FakerMaker


maker = FakerMaker()
print(maker.addrss(1))
