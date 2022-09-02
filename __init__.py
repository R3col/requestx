"""
title: Requestx
author: r3col
date: 2022-02-28
description: requests模块post参数会自动url编码，为了解决这个问题，只好自行动手封装urllib3库，提供类似于requests的接口和功能，并为渗透测试提供便利的特性
"""

from .models import Requestx, Responsex
from .api import get, head, post, patch, put, delete, options
