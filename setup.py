from setuptools import setup, find_packages

setup(name='EpigraphyScraper',
      version='0.1',
      description='Scraping http://db.edcs.eu/epigr/epi.php?s_sprache=en',
      url='https://github.com/Denubis/EpigraphyScraper',
      author='Denubis',
      author_email='brian.ballsun-stanton@mq.edu.au',
      license='MIT',      
      install_requires=[
          'beautifulsoup4',
          'MechanicalSoup',          
      ],
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      zip_safe=False)