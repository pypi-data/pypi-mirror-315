
from setuptools import setup, find_packages
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'newblackpink',        
  packages = ['newblackpink'],
  include_package_data=True,
  version = '1.0',    
  license='MIT',     
  description = 'Blackpink Logo Generator', 
  author = 'Piro Ayush',                  
  author_email = 'piroayush.tele@gmail.com',     
  url = 'https://github.com/PiroHackz/newblackpink',   
  download_url = 'https://github.com/PiroHackz/newblackpink/archive/0.1.tar.gz',    
  keywords = ['blackpink', 'logo', 'generator'], 
  install_requires=[           
          'pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
