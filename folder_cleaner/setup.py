from setuptools import setup


setup(
    name="folder_cleaner",
    version="V1.0",
    entry_points={
        'console_scripts': ['folder-cleaner=folder_cleaner.clean:main']
    },
    zip_safe=False,
    include_package_data=True,
    license='Public',
    description="Folder cleaner script",
)