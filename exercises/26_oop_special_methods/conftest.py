import re
import yaml
import pytest
from netmiko import ConnectHandler



def strip_empty_lines(output):
    lines = []
    for line in output.strip().split('\n'):
        line = line.strip()
        if line:
            lines.append(re.sub(' +', ' ', line.strip()))
    return '\n'.join(lines)


def test_attr_or_method(obj, attr=None, method=None):
    if attr:
        assert getattr(obj, attr, None) != None, "Атрибут не найден"
    if method:
        assert getattr(obj, method, None) != None, "Метод не найден"


@pytest.fixture()
def topology_with_dupl_links():
    topology = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}
    return topology


@pytest.fixture()
def normalized_topology_example():
    normalized_topology = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                           ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                           ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                           ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                           ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                           ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}
    return normalized_topology


@pytest.fixture(scope='module')
def first_router_from_devices_yaml():
    with open('devices.yaml') as f:
        devices = yaml.load(f)
        r1 = devices[0]
    return r1


@pytest.fixture(scope='module')
def r1_test_telnet_connection():
    with open('devices.yaml') as f:
        devices = yaml.load(f)
    r1_params = devices[0]
    options = {'device_type': 'cisco_ios_telnet',
               'timeout': 5,
               'fast_cli': True}
    r1_params.update(options)
    r1 = ConnectHandler(**r1_params)
    r1.enable()
    yield r1
    r1.disconnect()

