# Copyright (C) 2024 <UTN FRA>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from UTN_FRA import VERSION

setup(
    name= 'UTN_FRA',
    version=VERSION,
    description= 'Set de datos con informacion para trabajos y examenes',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author= 'Facundo Falcone',
    author_email="ffalcone@fra.utn.edu.ar",
    maintainer='Facundo Falcone',
    maintainer_email="ffalcone@fra.utn.edu.ar",
    url= 'https://pypi.org/project/UTN-FRA/',
    packages= find_packages(),
    py_modules=['UTN_FRA'],
    requires=['setuptools', 'tabulate'],
    install_requires=['setuptools', 'tabulate'],
    include_package_data=True,
    entry_points={
      'console_scripts': ['UTN_FRA=UTN_FRA.funciones:saludo']  
    },
    script_name='UTN_FRA:saludo',
    keywords=['UTN_FRA', 'UTN-FRA'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11'
)