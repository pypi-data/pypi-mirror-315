from setuptools import setup, find_packages

setup(
    name='voneska-mypackage',
    version='0.1',
    packages=find_packages(),
    description='Пример пакета с генераторами, итераторами, декораторами и дескрипторами',
    author='Владимир',
    author_email='ваш_email@example.com',
    url='https://example.com/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
