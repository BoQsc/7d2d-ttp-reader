"""
Player.ttp file reader.
Based on Karlovsky120's 7DaysProfileEditor
https://github.com/Karlovsky120/7DaysProfileEditor

Work in progress
"""


from struct import *

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

  def ReadInt16(self):
    return unpack('h', self.ReadBytes(2))[0]

  def ReadInt32(self):
    return unpack('i', self.ReadBytes(4))[0]

  def ReadSingle(self):
    return unpack('f', self.ReadBytes(4))[0]
    
  def ReadBoolean(self):
    return unpack('?', self.ReadBytes(1))[0]



class StreamReader(object):
  def __repr__(self):
    return '\n'.join(['{}:{}'.format(k,v) for k, v in vars(self).items()])
  

class Vector3D(object):
  def __repr__(self):
    return 'x:{}, y:{}, z:{}'.format(self.x, self.y, self.z)

class BodyDamage(StreamReader):
  def Read(self, reader):
    self.bodyDamageVersion = reader.ReadInt32()
    self.LeftUpperLeg = reader.ReadInt16()
    self.RightUpperLeg = reader.ReadInt16()
    self.LeftUpperArm = reader.ReadInt16()
    self.RightUpperArm = reader.ReadInt16()
    self.Chest = reader.ReadInt16()
    self.Head = reader.ReadInt16()
    self.DismemberedLeftUpperArm = reader.ReadBoolean()
    self.DismemberedRightUpperArm = reader.ReadBoolean()
    self.DismemberedHead = reader.ReadBoolean()
    self.DismemberedRightUpperLeg = reader.ReadBoolean()
    self.CrippledRightLeg = reader.ReadBoolean()
    
    self.LeftLowerLeg = reader.ReadInt16()
    self.RightLowerLeg = reader.ReadInt16()
    self.LeftLowerArm = reader.ReadInt16()
    self.RightLowerArm = reader.ReadInt16()
    self.DismemberedLeftLowerArm = reader.ReadBoolean()
    self.DismemberedRightLowerArm = reader.ReadBoolean()
    self.DismemberedLeftLowerLeg = reader.ReadBoolean()
    self.DismemberedRightLowerLeg = reader.ReadBoolean()

    self.DismemberedLeftLowerLeg = reader.ReadBoolean()
    self.CrippledLeftLeg = reader.ReadBoolean()

class StatModifier(StreamReader):
  def Read(self, reader):
    print('NOT IMPLIMENTED')

class Buff(StreamReader):
  def Read(self, reader, idTable):
    print('NOT IMPLIMENTED')
  
class Stat(StreamReader):
  def Read(self, reader, idTable):
    self.statVersion = reader.ReadInt32()
    self.value = reader.ReadSingle()
    self.maxModifier = reader.ReadSingle()
    self.valueModifier = reader.ReadSingle()
    self.baseMax = reader.ReadSingle()
    self.originalMax = reader.ReadSingle()
    self.originalValue = reader.ReadSingle()
    self.unknownG = reader.ReadBoolean()

    self.statModifierListCount = reader.ReadInt32()
    self.statModifierList = []
    for j in range(self.statModifierListCount):
      statModifier = StatModifier()
      statModifier.Read(reader)
      statModifier.stat = self
      self.statModifierList.append(statModifier)
      # TODO: do something with idtable
    

class EntityStats(StreamReader):
  def Read(self, reader):
    self.statsVersion = reader.ReadInt32()
    self.buffCategoryFlags = reader.ReadInt32() # TODO: Enumerate this

    self.immunityLength = reader.ReadInt32()
    self.immunity = []
    for i in range(self.immunityLength):
      self.immunity.append( reader.ReadInt32() )

    idTable = dict() # TODO: Figure this out
    self.health = Stat()
    self.health.Read(reader, idTable)
    self.stamina = Stat()
    self.stamina.Read(reader, idTable)
    self.sickness = Stat()
    self.sickness.Read(reader, idTable)
    self.gassiness = Stat()
    self.gassiness.Read(reader, idTable)
    self.speedModifier = Stat()
    self.speedModifier.Read(reader, idTable)
    self.wellness = Stat()
    self.wellness.Read(reader, idTable)
    self.coreTemp = Stat()
    self.coreTemp.Read(reader, idTable)
    self.food = Stat()
    self.food.Read(reader, idTable)
    self.water = Stat()
    self.water.Read(reader, idTable)
    self.waterLevel = reader.ReadSingle()

    self.buffListCount = reader.ReadInt32()
    self.buffList = []
    for j in range(self.buffListCount):
      buff = Buff()
      buff.Read(reader, idTable)
      self.buffList.append(buff)

    
    
    


class EntityCreationData(StreamReader):
  def Read(self, reader):
    self.entityCreationDataVersion = reader.ReadByte()
    self.entityClass = reader.ReadInt32()
    self.eid = reader.ReadInt32()
    self.lifetime = reader.ReadSingle()
    self.pos = Vector3D()
    self.pos.x = reader.ReadSingle()
    self.pos.y = reader.ReadSingle()
    self.pos.z = reader.ReadSingle()

    self.rot = Vector3D()
    self.rot.x = reader.ReadSingle()
    self.rot.y = reader.ReadSingle()
    self.rot.z = reader.ReadSingle()

    self.onGround = reader.ReadBoolean()

    self.bodyDamage = BodyDamage()
    self.bodyDamage.Read(reader)

    self.isStatsNotNull = reader.ReadBoolean()

    self.stats = EntityStats()
    self.stats.Read(reader)

    # self.deathTime = reader.ReadInt16()



class PlayerData(object):
  def __init__(self, filename):
    self.filename=filename
    
  def __repr__(self):
    return '\n'.join(['{}:{}'.format(k,v) for k, v in vars(self).items()])
   
  def Read(self):
    with open(self.filename, 'rb') as fin:
      reader = BinaryReader(fin)
      self.header = unpack('cccc', reader.ReadBytes(4))
      self.saveFileVersion = unpack('B', reader.ReadBytes(1))[0]

      self.ecd = EntityCreationData()
      self.ecd.Read(reader)
      # self.food = LiveStats()
      # self.food.Read(reader)
      # self.drink = LiveStats()
      # self.drink.Read(reader)





pd = PlayerData(FILE)
pd.Read()
  
print(pd)
  

  
