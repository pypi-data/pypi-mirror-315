from tinydb import TinyDB, Query
from pydantic import BaseModel

class PinConfiguration(BaseModel):
  ventilation_pwm_frequency : int = 20000 
  use_dht_22 : bool = False 
  thr1_active : bool = False
  thr2_active : bool = False 
  thr3_active : bool = False

class PinConfigurationStorage:
  db : TinyDB = None
  def __init__(self):
    self.db = TinyDB('pin_configuration-table.json')

  def update(self, configuration: PinConfiguration):
    self.db.truncate()
    self.db.insert(configuration.model_dump())

  def get(self) -> PinConfiguration:
    Qr = Query()
    if self.db.search(Qr.ventilation_pwm_frequency.exists()):
        print("finded!")
        data = self.db.all()[-1]
        return PinConfiguration(
           ventilation_pwm_frequency=data['ventilation_pwm_frequency'],
           use_dht_22=data['use_dht_22'],
           thr1_active=data['thr1_active'],
           thr2_active=data['thr2_active'],
           thr3_active=data['thr3_active']
        )
    else:
        print("empty")
        return PinConfiguration()
    
pinConfigurationStorage = PinConfigurationStorage()