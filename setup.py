from setuptools import setup

setup(name='EpigraphyScraper',
      version='0.1',
      description='Scraping http://db.edcs.eu/epigr/epi.php?s_sprache=en',
      url='https://github.com/Denubis/EpigraphyScraper',
      author='Denubis',
      author_email='brian.ballsun-stanton@mq.edu.au',
      license='MIT',
      packages=[''],
      install_requires=[
          'beautifulsoup4',
          'MechanicalSoup',          
      ],
      zip_safe=False)