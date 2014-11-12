import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'django',
    ]

setup(name='djinn_auth',
      version="1.0.2",
      description='Djinn Intranet auth module, role based',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "License :: Freely Distributable",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Site Management",
          "Topic :: Software Development :: Libraries :: "
          "Application Frameworks"
      ],
      author='PythonUnited',
      author_email='info@pythonunited.com',
      license='beer-ware',
      url='https://github.com/PythonUnited/djinn_auth',
      keywords='Djinn role base auth',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="djinn_auth",
      entry_points="""\
      [djinn.app]
      urls=djinn_auth:get_urls
      """
      )
