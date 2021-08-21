from setuptools import setup, find_packages

setup(name='lat-epig',
      version='2.0',
      description='This programme extracts the output of a search query from the [Epigraphik-Datenbank  Clauss / Slaby (EDCS)](http://www.manfredclauss.de/) in a reproducible manner and saves it as a TSV file. The output can be also plotted to a map of the Roman Empire, along with the system of Roman Provinces, roads, and cities.',
      url='https://github.com/mqAncientHistory/Lat-Epig',
      author='Brian Ballsun-Stanton',
      author_email='brian.ballsun-stanton@mq.edu.au',
      license='GPLv3',      
      install_requires=[
          "setuptools",
          "wheel",
          "numpy",
          "cython",
          "pyshp"         
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
        "Framework :: Jupyter",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research"
      ],
      project_urls={
        'Documentation': 'https://github.com/mqAncientHistory/Lat-Epig/wiki' ,               
        'Source': 'https://github.com/mqAncientHistory/Lat-Epig',
        'Tracker': 'https://github.com/mqAncientHistory/Lat-Epig/issues',
      },
      package_dir={'': 'src'},
      packages=find_packages(where='src'),      
      zip_safe=False,
      include_package_data=True
      
      ),