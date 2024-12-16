from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') #Gets the long description from Readme file

setup(
    name='xml_to_pandas',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],  # Add a comma here
    author='Pinak Tendulkar',
    author_email='pdtendulkar140203@gmail.com.com',
    description='Converts all kinds of XML files to a pandas dataframe',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/Pi2003/'
    }
)
