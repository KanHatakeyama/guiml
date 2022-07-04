from setuptools import setup, find_packages
import sys

sys.path.append('./guiml')

setup(name='guiml',
      version='0.0.3',
      description='guiml',
      long_description="README",
      author='Kan Hatakeyama',
      license="MIT",
      # packages=find_packages(),
      packages=[
          "guiml.Chem",
          "guiml.gui",
          "guiml.ml",
          "guiml",
      ],

      package_dir={
          "guiml.Chem": "guiml/Chem",
          "guiml.gui": "guiml/gui",
          "guiml.ml": "guiml/ml",
          "guiml": "guiml",
      },
      )
