from setuptools import setup, find_packages

setup(
    name="eval_python_2_mdhcquete_v3",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pillow",
        "matplotlib"
    ],
    entry_points={
        'console_scripts': [
            'eval_python_2_mdhcquete_v3=eval_python_2_mdhcquete_v3.main:main',
        ],
    },
    description="Evaluacion Python Nivel II",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marcos Daniel Herrera Cervantes",
    author_email="mrcsd.hrrr@gmail.com",
    url="https://github.com/mrcsd-hrrr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
