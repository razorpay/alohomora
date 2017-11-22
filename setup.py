from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='razorpay.alohomora',
      version='0.4.2',
      description='Secret distribution tool, written as a wrapper on credstash',
      url='http://github.com/razorpay/alohomora',
      author='Team Razorpay',
      author_email='developers@razorpay.com',
      keywords=["credstash", "ansible", "secrets", "jinja"],
      license='MIT',
      long_description=readme(),
      packages=['razorpay', 'razorpay.alohomora'],
      install_requires=[
          'credstash==1.13.3',
          'cryptography==2.0.3',
          'click==6.7',
          'jinja2==2.9.6',
          'botocore>1.7'
      ],
      entry_points={
          'console_scripts': [
              'alohomora = razorpay.alohomora.cli:cli'
          ]
      },
      package_dir={'razorpay.alohomora':  'razorpay/alohomora'},
      include_package_data=True,
      zip_safe=False
      )
