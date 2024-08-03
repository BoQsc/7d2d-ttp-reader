import struct
from collections import namedtuple
from typing import BinaryIO, Dict, Any

class BinaryReader:
    def __init__(self, buffer_object: BinaryIO):
        self._buffer_object = buffer_object

    def read_bytes(self, n: int) -> bytes:
        return self._buffer_object.read(n)

    def read_int8(self) -> int:
        return struct.unpack('b', self.read_bytes(1))[0]
    
    def read_uint8(self) -> int:
        return struct.unpack('B', self.read_bytes(1))[0]
    
    def read_int16(self) -> int:
        return struct.unpack('<h', self.read_bytes(2))[0]

    def read_uint16(self) -> int:
        return struct.unpack('<H', self.read_bytes(2))[0]

    def read_int32(self) -> int:
        return struct.unpack('<i', self.read_bytes(4))[0]

    def read_uint32(self) -> int:
        return struct.unpack('<I', self.read_bytes(4))[0]

    def read_single(self) -> float:
        return struct.unpack('<f', self.read_bytes(4))[0]
    
    def read_boolean(self) -> bool:
        return struct.unpack('?', self.read_bytes(1))[0]

    def read_string(self) -> str:
        length = self.read_uint16()
        byte_string = self.read_bytes(length)
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'ascii']:
            try:
                return byte_string.decode(encoding)
            except UnicodeDecodeError:
                continue
        # If all decodings fail, return a representation of the bytes
        return repr(byte_string)

    def seek(self, pos: int, whence: int = 0):
        self._buffer_object.seek(pos, whence)

    def skip(self, bytes_to_skip: int):
        self.seek(bytes_to_skip, 1)

Vector3d = namedtuple('Vector3d', ['x', 'y', 'z'])

Stat = namedtuple('Stat', ['version', 'value', 'max_modifier', 'value_modifier', 'base_max', 'original_max', 'original_value', 'unknown_g'])

BodyDamage = namedtuple('BodyDamage', [
    'body_damage_version', 'left_upper_leg', 'right_upper_leg', 'left_upper_arm',
    'right_upper_arm', 'chest', 'head', 'dismembered_left_upper_arm',
    'dismembered_right_upper_arm', 'dismembered_head', 'dismembered_right_upper_leg',
    'crippled_right_leg', 'left_lower_leg', 'right_lower_leg', 'left_lower_arm',
    'right_lower_arm', 'dismembered_left_lower_arm', 'dismembered_right_lower_arm',
    'dismembered_left_lower_leg', 'dismembered_right_lower_leg',
    'dismembered_left_upper_leg', 'crippled_left_leg'
])

def read_vector3d(reader: BinaryReader) -> Vector3d:
    return Vector3d(reader.read_single(), reader.read_single(), reader.read_single())

def read_stat(reader: BinaryReader) -> Stat:
    return Stat(
        version=reader.read_int32(),
        value=reader.read_single(),
        max_modifier=reader.read_single(),
        value_modifier=reader.read_single(),
        base_max=reader.read_single(),
        original_max=reader.read_single(),
        original_value=reader.read_single(),
        unknown_g=reader.read_single()
    )

def read_body_damage(reader: BinaryReader) -> BodyDamage:
    return BodyDamage(
        body_damage_version=reader.read_int32(),
        left_upper_leg=reader.read_int16(),
        right_upper_leg=reader.read_int16(),
        left_upper_arm=reader.read_int16(),
        right_upper_arm=reader.read_int16(),
        chest=reader.read_int16(),
        head=reader.read_int16(),
        dismembered_left_upper_arm=reader.read_boolean(),
        dismembered_right_upper_arm=reader.read_boolean(),
        dismembered_head=reader.read_boolean(),
        dismembered_right_upper_leg=reader.read_boolean(),
        crippled_right_leg=reader.read_boolean(),
        left_lower_leg=reader.read_int16(),
        right_lower_leg=reader.read_int16(),
        left_lower_arm=reader.read_int16(),
        right_lower_arm=reader.read_int16(),
        dismembered_left_lower_arm=reader.read_boolean(),
        dismembered_right_lower_arm=reader.read_boolean(),
        dismembered_left_lower_leg=reader.read_boolean(),
        dismembered_right_lower_leg=reader.read_boolean(),
        dismembered_left_upper_leg=reader.read_boolean(),
        crippled_left_leg=reader.read_boolean()
    )

def read_player_file(filename: str) -> Dict[str, Any]:
    player_info = {}
    with open(filename, 'rb') as fin:
        reader = BinaryReader(fin)
        
        player_info['header'] = reader.read_bytes(4)
        if player_info['header'] != b'ttp\x00':
            print(f"Warning: Unexpected file header: {player_info['header']}")
        
        player_info['save_file_version'] = reader.read_uint8()
        player_info['ecd_version'] = reader.read_uint8()

        player_info['entity_class'] = reader.read_int32()
        player_info['eid'] = reader.read_int32()
        player_info['lifetime'] = reader.read_single()

        player_info['position'] = read_vector3d(reader)
        player_info['rotation'] = read_vector3d(reader)
        
        player_info['is_on_ground'] = reader.read_boolean()

        player_info['body_damage'] = read_body_damage(reader)

        player_info['is_stats_not_null'] = reader.read_boolean()
        player_info['entity_stats_version'] = reader.read_int32()
        player_info['buff_category_flags'] = reader.read_int32()
        
        immunity_length = reader.read_int32()
        player_info['immunity'] = [reader.read_int32() for _ in range(immunity_length)]
        
        player_info['health'] = read_stat(reader)
        player_info['stamina'] = read_stat(reader)
        player_info['core_temperature'] = read_stat(reader)
        player_info['food'] = read_stat(reader)
        player_info['water'] = read_stat(reader)

        try:
            player_info['player_name'] = reader.read_string()
        except Exception as e:
            print(f"Warning: Error reading player name: {e}")
            player_info['player_name'] = "Unknown"

        try:
            player_info['equipped_items'] = []
            for _ in range(8):  # Assuming 8 equipment slots
                slot_id = reader.read_int32()
                item_name = reader.read_string() if slot_id != -1 else None
                player_info['equipped_items'].append((slot_id, item_name))
        except Exception as e:
            print(f"Warning: Error reading equipped items: {e}")

        try:
            player_info['skills'] = {}
            skills_count = reader.read_int32()
            for _ in range(skills_count):
                skill_name = reader.read_string()
                skill_level = reader.read_int32()
                player_info['skills'][skill_name] = skill_level
        except Exception as e:
            print(f"Warning: Error reading skills: {e}")

        try:
            player_info['perks'] = {}
            perks_count = reader.read_int32()
            for _ in range(perks_count):
                perk_name = reader.read_string()
                perk_level = reader.read_int32()
                player_info['perks'][perk_name] = perk_level
        except Exception as e:
            print(f"Warning: Error reading perks: {e}")

        try:
            player_info['buffs'] = {}
            buffs_count = reader.read_int32()
            for _ in range(buffs_count):
                buff_name = reader.read_string()
                buff_duration = reader.read_single()
                player_info['buffs'][buff_name] = buff_duration
        except Exception as e:
            print(f"Warning: Error reading buffs: {e}")

        try:
            player_info['additional_stats'] = {}
            additional_stats_count = reader.read_int32()
            for _ in range(additional_stats_count):
                stat_name = reader.read_string()
                stat_value = reader.read_single()
                player_info['additional_stats'][stat_name] = stat_value
        except Exception as e:
            print(f"Warning: Error reading additional stats: {e}")

    return player_info

if __name__ == "__main__":
    FILE = r'EOS_00020585a34f4b93bf8c21b3cf8d3150.ttp'
    player_info = read_player_file(FILE)
    for key, value in player_info.items():
        print(f"{key}: {value}")