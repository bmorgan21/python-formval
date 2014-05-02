from distutils.core import setup

setup(
    name='formval',
    version='0.1.0',
    author='Brian S Morgan',
    author_email='brian.s.morgan@gmail.com',
    packages=['formval'],
    url='https://github.com/bmorgan21/python-formval',
    description='Form validation library for Python.',
    install_requires=[
        'validation>=0.1.0'
    ]
)
