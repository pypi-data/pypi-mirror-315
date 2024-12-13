from setuptools import setup, find_packages

setup(
    name='combot_installer',
    version='0.1.0',
    description='A tool for automated installation',
    author='Hkcode',
    author_email='sissokoadel057@gmail.com',
    packages=find_packages(),  # Automatically find your packages
    include_package_data=True,  # Ensure non-Python files (like your scripts) are included
    install_requires=[],  # Any dependencies your package needs
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
)
