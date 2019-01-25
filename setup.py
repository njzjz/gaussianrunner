from setuptools import setup
setup(name='gaussianrunner',
      version='1.0.14',
      description='A script to run Gaussian automatically.',
      keywords="Gaussian",
      url='https://github.com/njzjz/gaussianrunner',
      author='Jinzhe Zeng',
      author_email='jzzeng@stu.ecnu.edu.cn',
      packages=['gaussianrunner'],
      install_requires=[],
      extras_require={
          "mpi":["mpi4py"]
      },
      test_suite='gaussianrunner.test',
      tests_require=[]
      )

