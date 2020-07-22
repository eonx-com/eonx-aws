from setuptools import setup

setup(
    name='eonx-aws',
    version='0.0.18',
    description='eonx-aws',
    url='git@github.com:eonx-com/eonx-aws.git',
    author='Damian Sloane',
    author_email='damian.sloane@eonx.com',
    license='unlicensed',
    packages=[
        'Aws',
        'Aws.Cloudwatch',
        'Aws.Ec2',
        'Aws.Ecs',
        'Aws.Lambda',
        'Aws.Logs',
        'Aws.Route53',
        'Aws.Sso',
        'Aws.Qldb'
    ],
    zip_safe=False,
    install_requires=['boto3']
)