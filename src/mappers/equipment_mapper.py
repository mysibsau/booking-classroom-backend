from models.equipment import Equipment
from schemas.equipment import EquipmentScheme


def pg_data_to_equipment_scheme_mapper(pg_data: Equipment) -> EquipmentScheme:

    return EquipmentScheme(
        id=str(pg_data.id),
        name=pg_data.equipment.name,
        description=pg_data.equipment.description,
        count=pg_data.count
    )
