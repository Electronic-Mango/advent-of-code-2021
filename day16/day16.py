from math import prod
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"

VERSION_LENGTH = 3
TYPE_LENGTH = 3
OPERATION_TYPE_LENGTH = 1
PACKET_HEADER = VERSION_LENGTH + TYPE_LENGTH

LITERAL_HEADER_LENGTH = PACKET_HEADER
LITERAL_TYPE = 4
LITERAL_GROUP_LENGTH = 5
LITERAL_GROUP_TYPE_LENGTH = 1
LITERAL_GROUP_TYPE_LAST = "0"

OPERATION_HEADER_LENGTH = PACKET_HEADER + OPERATION_TYPE_LENGTH
OPERATION_TYPE_LENGTH = 1
OPERATION_TYPE_0_ID = "0"
OPERATION_TYPE_0_LENGTH = 15
OPERATION_TYPE_1_LENGTH = 11

OPERATIONS = {
    0: lambda *values: sum(values),
    1: lambda *values: prod(values),
    2: lambda *values: min(values),
    3: lambda *values: max(values),
    5: lambda x, y: x > y,
    6: lambda x, y: x < y,
    7: lambda x, y: x == y,
}

VERSIONS = []


def load_bits():
    with open(get_input_file_name()) as input_file:
        return input_file.readline().strip()


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(hex_bits):
    print(f"Running task 1...")
    packet = hex_to_bin(hex_bits)
    result, _ = handle_packet(packet)
    print(f"Sum of all versions: {sum(VERSIONS)} == 936 {sum(VERSIONS) == 936}")
    print(f"Final result: {result} == 6802496672062 {result == 6802496672062}")
    print()


def hex_to_bin(bits):
    number_of_bits = len(bits) * 4
    bits_hex = int(bits, 16)
    bits_bin = bin(bits_hex)
    return bits_bin[2:].zfill(number_of_bits)


def handle_packet(packet):
    version, type, remaining_bits = parse_version_type(packet)
    VERSIONS.append(version)
    if type == LITERAL_TYPE:
        return handle_literal(remaining_bits)
    else:
        return handle_operation(remaining_bits, OPERATIONS[type])


def parse_version_type(bits):
    version = int(bits[:VERSION_LENGTH], 2)
    type = int(bits[VERSION_LENGTH : VERSION_LENGTH + TYPE_LENGTH], 2)
    return version, type, bits[VERSION_LENGTH + TYPE_LENGTH :]


def handle_literal(literal_bits):
    literal_groups = []
    literal_bits = handle_literal_group(literal_bits, literal_groups)
    while literal_groups[-1][:LITERAL_GROUP_TYPE_LENGTH] != LITERAL_GROUP_TYPE_LAST:
        literal_bits = handle_literal_group(literal_bits, literal_groups)
    literal_segments = [group[LITERAL_GROUP_TYPE_LENGTH:] for group in literal_groups]
    literal = "".join(literal_segments)
    offset = PACKET_HEADER + len(literal_segments) + len(literal)
    return int(literal, 2), offset


def handle_literal_group(literal_bits, literal_groups):
    literal_group = literal_bits[:LITERAL_GROUP_LENGTH]
    literal_groups.append(literal_group)
    return literal_bits[LITERAL_GROUP_LENGTH:]


def handle_operation(bits, operation):
    operation_type, remaining_bits = bits[:OPERATION_TYPE_LENGTH], bits[OPERATION_TYPE_LENGTH:]
    subpackets_size_length = get_subpacket_size_length(operation_type)
    subpackets_size = int(remaining_bits[:subpackets_size_length], 2)
    values = []
    if operation_type == OPERATION_TYPE_0_ID:
        offset = operation_type_0(remaining_bits, subpackets_size, subpackets_size_length, values)
    else:
        offset = operation_type_1(remaining_bits, subpackets_size, subpackets_size_length, values)
    return operation(*values), offset + OPERATION_HEADER_LENGTH


def get_subpacket_size_length(type):
    return OPERATION_TYPE_0_LENGTH if type == OPERATION_TYPE_0_ID else OPERATION_TYPE_1_LENGTH


def operation_type_0(bits, length_of_subpackets, offset, values):
    while offset < length_of_subpackets + OPERATION_TYPE_0_LENGTH:
        offset += handle_subpackets(offset, values, bits)
    return offset


def operation_type_1(bits, number_of_subpackets, offset, values):
    for _ in range(number_of_subpackets):
        offset += handle_subpackets(offset, values, bits)
    return offset


def handle_subpackets(offset, values, bits):
    value, new_offset = handle_packet(bits[offset:])
    values.append(value)
    return new_offset


bits = load_bits()
task(bits)
