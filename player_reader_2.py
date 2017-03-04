"""
Player.ttp player tracker.
Based on Karlovsky120's 7DaysProfileEditor
https://github.com/Karlovsky120/7DaysProfileEditor

Work in progress
"""


from struct import *
import struct
from collections import namedtuple

# replace with file to read (I currently have this hardcoded while testing.)
FILE=r'XXXXXXXXXXXXXXXXX.ttp'

class BinaryReader(object):
  def __init__(self, buffer_object):
    self._buffer_object=buffer_object

  def ReadChar(self):
    return unpack('c', self._buffer_object.read(1))[0]

  def ReadByte(self):
    return unpack('c', self._buffer_object.read(1))[0]

  def ReadBytes(self, n):
    return self._buffer_object.read(n)

  def ReadInt8(self):
    return unpack('b', self.ReadBytes(1))[0]
  
  def ReadUInt8(self):
    return unpack('B', self.ReadBytes(1))[0]
  
  def ReadInt16(self):
    return unpack('h', self.ReadBytes(2))[0]

  def ReadUInt16(self):
    return unpack('H', self.ReadBytes(2))[0]

  def ReadInt32(self):
    return unpack('i', self.ReadBytes(4))[0]

  def ReadSingle(self):
    return unpack('f', self.ReadBytes(4))[0]
    
  def ReadBoolean(self):
    return unpack('?', self.ReadBytes(1))[0]

  def ReadCustom(self, struct_fmt):
    return struct.unpack(struct_fmt,
                         self._buffer_object.read(
                           struct.calcsize( struct_fmt ) ) )

  def Seek(self, pos, whence=0):
    self._buffer_object.seek(pos, whence)

  def Skip(self, _bytes):
    self.Seek(_bytes, 1)

STRUCT_FMT_VECTOR3D='<fff'
Vector3d = namedtuple('Vector3d', ['x', 'y', 'z'])

STRUCT_FMT_STAT='<lfffffff'
Stat = namedtuple('Stat', [ 'version','value', 'max_modifier',
                                      'value_modifier', 'base_max',
                                      'original_max', 'original_value', 'unknown_g'])

STRUCT_FMT_BODYDAMAGE='<ihhhhhh?????hhhh??????'
BodyDamage = namedtuple('BodyDamage',
                        ['body_damage_version',
                         'left_upper_leg',
                         'right_upper_leg',
                         'left_upper_arm',
                         'right_upper_arm',
                         'chest',
                         'head',
                         'dismembered_left_upper_arm',
                         'dismembered_right_upper_arm',
                         'dismembered_head',
                         'dismembered_right_upper_leg',
                         'crippled_right_leg',
                         'left_lower_leg',
                         'right_lower_leg',
                         'left_lower_arm',
                         'right_lower_arm',
                         'dismembered_left_lower_arm',
                         'dismembered_right_lower_arm',
                         'dismembered_left_lower_leg',
                         'dismembered_right_lower_leg',
                         'dismembered_left_upper_leg',
                         'crippled_left_leg']
                        )
                         
                                       


def read_player_file(filename):
  player_info = {}
  with open(filename, 'rb') as fin:
    reader = BinaryReader(fin)
    player_info['header'] = reader.ReadBytes(4)
    assert (player_info['header'] == b'ttp\x00'), 'File header missmatch: {}'.format(filename)
    player_info['save_file_version'] = reader.ReadUInt8()
    assert (player_info['save_file_version'] == 34), 'File version missmatch: {}'.format(filename)
    player_info['ecd_version'] = reader.ReadUInt8()
    assert (player_info['ecd_version'] == 25), 'ECD version missmatch: {}'.format(filename)

    player_info['entity_class'] = reader.ReadInt32()
    player_info['eid'] = reader.ReadInt32()
    player_info['lifetime'] = reader.ReadSingle()

    player_info['position'] = Vector3d._make(
        reader.ReadCustom(STRUCT_FMT_VECTOR3D ) )
    player_info['rotation'] = Vector3d._make(
        reader.ReadCustom(STRUCT_FMT_VECTOR3D ) )
    
    player_info['is_on_ground'] = reader.ReadBoolean()

    player_info['body_damage'] = BodyDamage._make(
      reader.ReadCustom(STRUCT_FMT_BODYDAMAGE ) )

    player_info['is_stats_not_null'] = reader.ReadBoolean()
    player_info['entity_stats_version'] = reader.ReadInt32()
    player_info['buff_category_flags'] = reader.ReadInt32() # TODO: Enumerate this
    immunityLength = reader.ReadInt32()

    player_info['immunity'] = reader.ReadCustom( 'i' * immunityLength)
    player_info['health'] = Stat._make(reader.ReadCustom(STRUCT_FMT_STAT))
    
    return player_info
    



player_info = read_player_file(FILE)
print(player_info)
