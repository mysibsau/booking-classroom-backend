from models.room import Room
from schemas.room import RoomScheme
from mappers.equipment_mapper import pg_data_to_equipment_scheme_mapper


def pg_data_to_room_scheme_mapper(pg_data: Room) -> RoomScheme:

    return RoomScheme(
        id=pg_data.id,
        photo=pg_data.photo,
        description=pg_data.description,
        address=pg_data.address,
        capacity=pg_data.capacity,
        equipment=[
            pg_data_to_equipment_scheme_mapper(equip)
            for equip in pg_data.equipment
        ]
    )
