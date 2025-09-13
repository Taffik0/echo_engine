from src.registers.registers import Register, RegisterRecord

from src.entities.orb import Orb


class OrbRegister(Register):
    pass


orb_register = OrbRegister()
orb_register.add_record_list([(RegisterRecord(Orb, "BlueOrb"), 100)])
