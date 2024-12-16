from setuptools import setup, find_packages

setup(
name='stay_online',
version='0.1.2',
author='Chiaope',
author_email='',
description='Simulate fake mouse and keyboard actions to fake staying online',
install_requires=[
    'pyautogui',
    'pynput'
    ],
packages=find_packages(),
package_data={'': ['word_file.txt']},
include_package_data=True,
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.8',
)
