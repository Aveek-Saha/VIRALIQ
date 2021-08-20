import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='viraliq',
    version='0.1.2',
    author="Aveek Saha",
    author_email="aveek.s98@gmail.com",
    url='https://github.com/Aveek-Saha/VIRALIQ',
    description="Search for videos using an image query.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages= setuptools.find_packages(),
    include_package_data=True,
    py_modules=['viraliq'],
    install_requires=[
        'Click',
        'tensorflow==2.6.0',
        'scikit_learn',
        'numpy',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'viraliq = viraliq:cli',
        ],
    },
)