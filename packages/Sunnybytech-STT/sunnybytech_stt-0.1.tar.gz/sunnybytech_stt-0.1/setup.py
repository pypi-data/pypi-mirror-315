from setuptools import setup, find_packages

setup(
    name='Sunnybytech_STT',
    version='0.1',
    author='Sunil Kahar',
    author_email='sunilkhr1921@gmail.com',
    description='This is a speech-to-text package created by Sunil Kahar',
    packages=find_packages(),  # Note the correct usage of this
    install_requires=[  # Corrected the parameter name
        'selenium',
        'webdriver-manager'  # Fixed spelling
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specifies minimum Python version
)

