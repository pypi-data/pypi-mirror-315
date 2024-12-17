from setuptools import setup, find_packages

setup(
    name='retrolib',
    version='0.3.1',
    packages=find_packages(),
    install_requires=[
        "Pillow",
    ],
    author='Léonor Leclerc',
    author_email='leo-nor7777@outlook.com',
    description='Une bibliothèque avec des trucs retro. A library with retro stuff.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.4',
)
