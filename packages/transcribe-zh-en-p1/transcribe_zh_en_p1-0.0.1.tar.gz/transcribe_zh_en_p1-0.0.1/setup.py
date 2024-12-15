from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='transcribe_zh_en_p1',
    version='0.0.1',
    packages=find_packages(),  # Automatically find all submodules
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'transcribe_zh_en = transcribe_zh_en.main:main',  # Entry point to the main function
        ],
    },
    author="Mousa Abdulhamid",
    author_email="mousa.abdulhamid97@gmail.com",
    description="This package is a part of a larger pipeline. This is package (PART:1). A package to convert Video containing spoken Chinese audio and Chinese written text and convert it into spoken English and English written text.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abdulhamid97Mousa/transcribe_zh_en_p1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8, <3.9',
)