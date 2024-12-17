from setuptools import setup, find_packages

setup(
    name="kiam_astro",
    version="5.0.4",
    author="Maksim Shirobokov",
    author_email="shmaxg@gmail.com",
    description='KIAM Astrodynamics Toolbox',
    long_description='Astrodynamics toolbox for fundamental research and education.',
    keywords=['astrodynamics', 'spacecraft', 'mission analysis'],
    python_requires='>=3.9,<3.14',
    packages=find_packages(),
    package_data={'kiam_astro': ['/Users/shmaxg/Yandex.Disk.localized/Python/KIAMToolbox/kiam_astro/*']},
    include_package_data=True,
    install_requires=[
        "numpy>=2.0,<3.0",
        "jdcal",
        "networkx",
        "scipy",
        "plotly",
        "kaleido; platform_system != 'Windows'",  # для macOS и Linux - любая версия
        "kaleido==0.1.0.post1; platform_system == 'Windows'",  # для Windows - фиксированная версия
        "pillow"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Fortran",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ]
)
