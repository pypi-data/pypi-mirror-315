from setuptools import setup, find_packages

setup(
    name='lomefaire',  # Replace with your package’s name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    author='lomefaire',  
    author_email='lomefaire@gmail.com',
    description='Test',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',

)