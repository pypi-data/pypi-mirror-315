from setuptools import setup, find_packages

setup(
name='stay_online',
version='0.1.0',
author='Chiaope',
author_email='',
description='Simulate fake mouse and keyboard actions to fake staying online',
packages=find_packages(
    'pyautogui',
    'pynput'
),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)