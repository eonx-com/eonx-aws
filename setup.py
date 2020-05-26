from setuptools import setup

setup(
    name='eonx-aws',
    version='0.0.4',
    description='eonx-aws',
    url='git@github.com:eonx-com/eonx-aws.git',
    author='Damian Sloane',
    author_email='damian.sloane@eonx.com',
    license='unlicensed',
    packages=[
        'Aws',
        'Aws.Cloudwatch',
        'Aws.Ecs',
        'Aws.Lambda',
        'Aws.Sso'
    ],
    zip_safe=False,
    install_requires=['boto', 'boto3', 'botocore']
)