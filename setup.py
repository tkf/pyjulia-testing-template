from setuptools import setup, find_packages

setup(
    name='pyjulia-testing-template',
    version="0.0.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Takafumi Arakaki',
    author_email='aka.tkf@gmail.com',
    # url='https://github.com/tkf/pyjulia-testing-template',
    license='MIT',  # SPDX short identifier
    # description='pyjulia-testing-template - THIS DOES WHAT',
    long_description=open('README.rst').read(),
    # keywords='KEYWORD, KEYWORD, KEYWORD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        'julia',
    ],
)
