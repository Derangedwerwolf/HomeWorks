from setuptools import setup, find_namespace_packages

setup(
    name='ClassBotExtended',
    version='V1.0',
    description='bot assistant',
    entry_points={'console_scripts': [
        'contact_book = ContactBook.main:main']},
    url='https://github.com/Laplas00/ContactBook',
    author='Omelchenko Igor'
    author_email='Nitro-zet@ukr.net',
    license='Public',
    include_package_data=True,
    packages=find_namespace_packages()
    )