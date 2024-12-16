from setuptools import setup, find_packages

setup(
    name='cool-booy-tmux',
    version='1.1.1',
    description='A tmux setup script for customizing tmux configurations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='IM COOL BOOY',
    author_email='coolbooy@gmail.com',
    url='https://github.com/IM-COOL-HACKER-BOOY/cool-booy-tmux',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'cool-booy-tmux=cool_booy_tmux:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
