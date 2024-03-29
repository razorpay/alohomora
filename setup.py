from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='razorpay.alohomora',
    version='0.5.0',
    description='Secret distribution tool, written as a wrapper on credstash',
    url='https://github.com/razorpay/alohomora',
    author='Team Razorpay',
    author_email='developers@razorpay.com',
    tests_require=['pytest', 'pytest-runner'],
    test_suite='tests',
    keywords=["credstash", "ansible", "secrets", "jinja"],
    license='MIT',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    packages=find_packages(exclude=('tests')),
    python_requires='>=3.7.0',
    install_requires=[
        'credstash==1.17.1',
        'click>=8.1',
        'jinja2>=3.0',
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
