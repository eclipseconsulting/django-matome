from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    "Programming Language :: Python",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django'
]

setup(
    author='Keita Oouchi',
    author_email='keita.oouchi@gmail.com',
    url='https://github.com/keitaoouchi/django-matome',
    name='django-matome',
    version='0.0.1',
    packages=['matome', 'matome.management', 'matome.management.commands'],
    license='BSD License',
    classifiers=classifiers,
    description='Report code statistics (KLOCs, etc) from the django project.',
    install_requires=[
        'Django>=1.4',
    ],
    # Packaging options:
    zip_safe=False,
    include_package_data=True
)
