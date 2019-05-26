#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pyanote

setup(
   name='pyanote',
   version='0.0.2-beta.1',
   description='Un projet ISN de manipulation de fichiers MIDI.',
   author='Lisa Baget and Matthieu Durand',
   author_email='li.baget@laposte.net',
   packages=find_packages(), 
   install_requires=['pygame']
)
