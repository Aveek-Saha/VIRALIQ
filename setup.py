from setuptools import setup

setup(
    name='viraliq',
    version='0.1.0',
    py_modules=['viraliq'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'viraliq = viraliq:cli',
        ],
    },
)