from setuptools import setup, find_packages

with open('pipeline_req.yml', 'r') as f:
    requirements = f.readlines()

install_req = []
for requirement in requirements:
    if requirement == '': break
    package_info = requirement.split('=')
    package_name = package_info[0][4:]
    if package_name[0] == '_': continue
    if 'jupyter' in package_name: continue
    package_vers = package_info[1]
    if len(package_vers.split('.')) < 2: continue
    if package_vers == '': package_vers = package_info[2][:-1]
    install_req.append(package_name+'=='+package_vers)

setup(
    name='zebrafishBlood',
    version='0.1',
    description='Zebrafish blood smear cell counter',
    author=['Eunhye Yang'],
    author_email='eunhye@connect.hku.hk',
    packages=find_packages(),
    install_requires=install_req
)