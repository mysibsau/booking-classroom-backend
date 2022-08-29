from models.equipment import Equipment
from schemas.equipment import EquipmentScheme


def pg_data_to_equipment_scheme_mapper(pg_data: Equipment) -> EquipmentScheme:

    return EquipmentScheme(
        name=pg_data.equipment.name,
        description=pg_data.equipment.description,
        count=pg_data.count
    )
