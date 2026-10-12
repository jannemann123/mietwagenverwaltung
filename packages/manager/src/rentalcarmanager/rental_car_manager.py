from __future__ import annotations
from typing import Iterable, Protocol
from dataclasses import dataclass


from rentalcarui.rental_car_ui import  IManager, Car, Customer


from rentalcarmanager.types import LicensePlate, CustomerID, CUSTOMER_ID_UNSET


class RentalException(Exception): pass


@dataclass(frozen=True)
class CarData:
    license_plate: LicensePlate
    manufacturer: str
    model: str
    rented_by_customer: CustomerID


@dataclass(frozen=True)
class CustomerData:
    name: str
    identifier: CustomerID


# ---------------------------------------------------------
# 3. DAS STORAGE INTERFACE (Das Storage-Package richtet sich hiernach)
# ---------------------------------------------------------
class IStorage(Protocol):
    def close(self) -> None: ...

    def get_cars(self) -> Iterable[CarData]: ...

    def get_car(self, license_plate: LicensePlate) -> CarData: ...

    def add_car(self, car: CarData) -> None: ...

    def delete_car(self, license_plate: LicensePlate) -> None: ...

    def update_car(self, car: CarData) -> None: ...

    def get_customers(self) -> Iterable[CustomerData]: ...

    def get_customer(self, customer_id: CustomerID) -> CustomerData: ...

    def add_customer(self, customer: CustomerData) -> None: ...

    def delete_customer(self, customer_id: CustomerID) -> None: ...

    def update_customer(self, customer: CustomerData) -> None: ...


# ---------------------------------------------------------
# 4. DEIN MANAGER
# Erbst jetzt von IManager aus dem UI-Package!
# ---------------------------------------------------------
class RentalCarManager(IManager):
    __storage: IStorage

    def __init__(self, storage: IStorage) -> None:
        self.__storage = storage
        # Der Logger ist laut UML im UI-Package. Der Manager loggt selbst nicht mehr.

    def get_cars(self) -> Iterable[Car]:
        cars = []
        for data in self.__storage.get_cars():
            car = Car(
                data.license_plate,
                data.manufacturer,
                data.model,
                rented_by_customer=data.rented_by_customer
            )
            cars.append(car)
        return cars

    # Gibt Iterable[Customer] (UI-Objekte) zurück
    def get_customers(self) -> Iterable[Customer]:
        return [
            Customer(data.name, data.identifier)
            for data in self.__storage.get_customers()
        ]

    # Beachte: Das UML sagt hier (customer_id: int) und nicht CustomerID!
    def rent_car(self, customer_id: int, car_model: str) -> None:
        customer_data = self.__storage.get_customer(customer_id)

        available_cars = [
            car for car in self.__storage.get_cars()
            if car.model == car_model and car.rented_by_customer == CUSTOMER_ID_UNSET
        ]
        if not available_cars:
            raise RentalException(f"Model is unavailable: {car_model}")

        # Wir nehmen das erste verfügbare Auto und updaten es
        car_to_rent = available_cars[0]

        # Da CarData "frozen=True" (unveränderlich) ist, erstellen wir ein neues
        updated_car = CarData(
            license_plate=car_to_rent.license_plate,
            manufacturer=car_to_rent.manufacturer,
            model=car_to_rent.model,
            rented_by_customer=customer_id
        )
        self.__storage.update_car(updated_car)

    def return_car(self, license_plate: str) -> None:
        car_data = self.__storage.get_car(license_plate)

        if car_data.rented_by_customer == CUSTOMER_ID_UNSET:
            raise RentalException(f"Car was not rented: {license_plate}")

        updated_car = CarData(
            license_plate=car_data.license_plate,
            manufacturer=car_data.manufacturer,
            model=car_data.model,
            rented_by_customer=CUSTOMER_ID_UNSET
        )
        self.__storage.update_car(updated_car)

    def add_car(self, license_plate: str, manufacturer: str, model: str) -> None:
        # Hier geben wir direkt ein CarData an das Storage weiter
        new_car_data = CarData(license_plate, manufacturer, model, CUSTOMER_ID_UNSET)
        self.__storage.add_car(new_car_data)

    def remove_car(self, license_plate: str) -> None:
        car = self.__storage.get_car(license_plate)
        if car.rented_by_customer != CUSTOMER_ID_UNSET:
            raise RentalException(f"Car '{license_plate}' is currently rented.")

        self.__storage.delete_car(license_plate)

    def add_customer(self, customer_name: str) -> None:
        new_customer_data = CustomerData(customer_name, CUSTOMER_ID_UNSET)
        self.__storage.add_customer(new_customer_data)

    def remove_customer(self, customer_id: int) -> None:
        # Check ob der Kunde noch Autos hat
        if any(car.rented_by_customer == customer_id for car in self.__storage.get_cars()):
            raise RentalException(f"Customer '{customer_id}' has not returned all cars yet")

        self.__storage.delete_customer(customer_id)