from setuptools import setup, find_packages

setup(
    name='Sunnybytech_STT',
    version='1.0',
    author='Sunil Kahar',
    author_email='sunilkhr1921@gmail.com',
    description='This is a speech-to-text package created by Sunil Kahar',
    packages=find_packages(),  # Note the correct usage of this
    install_requires=[  # Corrected the parameter name
        'selenium',
        'webdriver-manager'  # Fixed spelling
    ],
        long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sunilkahar19',  # Update to your GitHub repo if available
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
   
    
    python_requires='>=3.8',
    license='MIT',
)

