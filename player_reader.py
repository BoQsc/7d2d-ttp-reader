"""
Player.ttp file reader.
Based on Karlovsky120's 7DaysProfileEditor
https://github.com/Karlovsky120/7DaysProfileEditor

Work in progress
"""


from struct import *

# replace with file to read (I currently have this hardcoded while testing.)
FILE=r'EOS_00020585a34f4b93bf8c21b3cf8d3150.ttp'

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



class SaveObject(object):
  def __repr__(self):
    return '\n'.join(['{}:{}'.format(k,v) for k, v in vars(self).items()])
  def Read(self, reader, *args, **kwargs):
    if callable(getattr(self, '_Read', None)):
      print('!!! {} NOT COMPLETED'.format(self.__class__.__name__))
      self._Read( reader, *args, **kwargs)
      
    else:
      print('!!!!! {} NOT IMPLIMENTED'.format(self.__class__.__name__))

  


class BaseObjective(SaveObject):
  currentValue = None #byte
  currentVersion = None # byte
  def Read(self, reader):
    self.currentVersion = reader.ReadByte()
    self.currentValue = reader.ReadByte()

class BodyDamage(SaveObject):
  bodyDamageVersion = None # int
  Chest = None # bool
  CrippledLeftLeg = None # bool
  CrippledRightLeg = None # bool
  DismemberedHead = None # bool
  DismemberedLeftLowerArm = None # bool
  DismemberedLeftLowerLeg = None # bool
  DismemberedLeftUpperArm = None # bool
  DismemberedLeftUpperLeg = None # bool
  DismemberedRightLowerArm = None # bool
  DismemberedRightLowerLeg = None # bool
  DismemberedRightUpperArm = None # bool
  DismemberedRightUpperLeg = None # bool
  Head = None # int
  LeftLowerArm = None # int
  LeftLowerLeg = None # int
  LeftUpperArm = None # int
  LeftUpperLeg = None # int
  RightLowerArm = None # int
  RightLowerLeg = None # int
  RightUpperArm = None # int
  RightUpperLeg = None # int

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


class Buff(SaveObject):
  buffClassId = None # int
  buffVersion = None # int
  # TODO: Need to set this dictionary
  dictionary = {} # EnumBuffClassId
  buffModifierList = [] # BuffModifier
  descriptor = None # BuffDescriptor
  instigatorId = None #int
  isOverriden = None # Bool
  statModifierList = [] # StatModifier
  timer = None # BuffTimer
  
  def _Read(self, reader, idTable, buffVersion=None):
    if buffVersion is None:
      self.buffVersion = reader.ReadUInt16()
      self.buffClassId = reader.ReadByte()
      #_type = self.dictionary.get(self.buffClassId)
      buff = Buff()
      buff.Read(reader, idTable, buffVersion=self.buffVersion)
      return buff
    else:
      self.timer = BuffTimer()
      self.timer.Read(reader)
      self.descriptor = BuffDescriptor()
      self.descriptor.Read(reader)
      self.isOverridden = reader.ReadBoolean()
      self.statModifierListCount = reader.ReadUInt8()
      self.statModifierList = []
      for i in range(self.statModifierListCount):
        key = reader.ReadUInt16()
        statModifier = idTable[key] # TODO: this will break
        self.statModifierList.append(statModifier)

      self.buffModifierListCount = reader.ReadUInt8()
      self.buffModifierList = []
      for j in range(self.buffModifierListCount):
        buffModifier = BuffModifier()
        buffModifier.Read(reader)
        buffModifier.buff = self
        buffModifierList.append(buffModifier)
      self.instigatorID = reader.ReadInt32()


class BuffDescriptor(SaveObject):
  pass

class BuffModifier(SaveObject):
  pass

class BuffTimer(SaveObject):
  pass

class BuffTimer(SaveObject):
  pass
      
class BuffTimerDuration(SaveObject):
  pass

class BuffTimerNull(SaveObject):
  pass

class BuffTimerScheduled(SaveObject):
  pass

class Colour(SaveObject):
  pass

class CraftingData(SaveObject):
  pass

class EntityCreationData(SaveObject):
    
  def _Read(self, reader):
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


class EntityStats(SaveObject):
  def _Read(self, reader):
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

class EnumBuffCategoryFlags(SaveObject):
  pass
class EnumBuffClassId(SaveObject):
  pass
class EnumBuffTimerClassId(SaveObject):
  pass
class EnumSpawnerSource(SaveObject):
  pass
class EnumStatModifierClassId(SaveObject):
  pass
class Equipment(SaveObject):
  pass
class IValueListener(SaveObject):
  pass
class ItemStack(SaveObject):
  pass
class ItemValue(SaveObject):
  pass
class JournalEntry(SaveObject):
  pass
class LiveStats(SaveObject):
  pass

class Multibuff(SaveObject):
  pass
class MultibuffAction(SaveObject):
  pass
class MultibuffPrefabAttachmentDescriptor(SaveObject):
  pass
class MultibuffVariable(SaveObject):
  pass
class PlayerDataFile(SaveObject):
  pass
class PlayerJournal(SaveObject):
  pass
class PlayerProfile(SaveObject):
  pass
class Quest(SaveObject):
  pass
class QuestJournal(SaveObject):
  pass
class Recipe(SaveObject):
  pass
class RecipeQueueItem(SaveObject):
  pass
class Skill(SaveObject):
  pass
class Skills(SaveObject):
  pass

 
class Stat(SaveObject):
  def _Read(self, reader, idTable):
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

class StatModifier(SaveObject):
  pass
class StatModifierMax(SaveObject):
  pass
class StatModifierModifyValue(SaveObject):
  pass
class StatModifierMulValue(SaveObject):
  pass
class StatModifierSetValue(SaveObject):
  pass
class StatModifierValueOT(SaveObject):
  pass

class TileEntityLootContainer(SaveObject):
  pass

class Utils(SaveObject):
  pass
class Value(SaveObject):
  pass

class Vector3D(object):
  def __repr__(self):
    return 'x:{}, y:{}, z:{}'.format(self.x, self.y, self.z)

class Waypoint(SaveObject):
  pass
class WaypointCollection(SaveObject):
  pass


    
    
    

class PlayerData(object):
  def __init__(self, filename):
    self.filename=filename
    
  def __repr__(self):
    return '\n'.join(['{}:{}'.format(k,v) for k, v in vars(self).items()])
   
  def Read(self):
    with open(self.filename, 'rb') as fin:
      reader = BinaryReader(fin)
      self.header = unpack('cccc', reader.ReadBytes(4))
      self.saveFileVersion = reader.ReadUInt8()

      self.ecd = EntityCreationData()
      self.ecd.Read(reader)
      # self.food = LiveStats()
      # self.food.Read(reader)
      # self.drink = LiveStats()
      # self.drink.Read(reader)





pd = PlayerData(FILE)
pd.Read()
  
print(pd)
  

  
