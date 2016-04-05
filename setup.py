from distutils.core import setup

setup(
    name='formval21',
    packages=['formval21'],
    version='0.2.0',
    description='Form validation library for Python.',
    author='Brian S Morgan',
    author_email='brian.s.morgan@gmail.com',
    url='https://github.com/bmorgan21/python-formval',
    install_requires=[
        'validation21>=0.2.1',
        'Werkzeug>=0.9.4',
        'Pillow>=2.4.0'
    ]
)
