from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='razorpay.alohomora',
      version='0.1',
      description='Secret distribution tool, written as a wrapper on credstash',
      url='http://github.com/razorpay/alohomora',
      author='Team Razorpay',
      author_email='developers@razorpay.com',
      keywords=["credstash", "ansible", "secrets", "jinja"],
      license='MIT',
      long_description=readme(),
      packages=['razorpay.alohomora'],
      install_requires=[
          'credstash',
          'click',
          'jinja2'
      ],
      include_package_data=True,
      zip_safe=False,
      scripts=['razorpay/alohomora/cli'],
      )
