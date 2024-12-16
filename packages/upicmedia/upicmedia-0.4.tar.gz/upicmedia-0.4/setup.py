from setuptools import setup, find_packages

setup(
    name='upicmedia',             
    version='0.4',                 
    packages=find_packages(),      
    description='Python package to get data from the UPIC service with crowdsourced tools',   
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    author='Mehrdad Rashidian',            
    author_email='Mehrdadrashidian70@gmail.com', 
    url='https://github.com/upicmi/Upicmedia',  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
    install_requires=[]      
)
