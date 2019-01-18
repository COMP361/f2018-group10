from src.constants.enums.VehicleKindEnum import VehicleKindEnum


class ParkingSpotModel(object):

    def __init__(self, vehicle_kind: VehicleKindEnum):
        self._vehicle_kind = vehicle_kind
