#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 00:30:24 2023

@author: dev
"""

from predict_new_cat import user_view, admin_view

admin = 0
admin = int(input('Press 1 if admin, 0 if user\n'))

if admin:
    admin_view()
else:
    user_view()
