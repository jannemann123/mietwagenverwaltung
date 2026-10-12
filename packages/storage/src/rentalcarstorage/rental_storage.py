from __future__ import annotations
import shelve
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, ClassVar

from .exceptions import RentalException

from rentalcarmanager.rental_car_manager import CarData, CustomerData, IStorage
from rentalcarmanager.rental_car_manager import LicensePlate, CustomerID


@dataclass
class StorageData:
    cars: dict[LicensePlate, CarData] = field(default_factory=dict)
    customers: dict[CustomerID, CustomerData] = field(default_factory=dict)
    customer_id_counter: int = 0

class RentalStorage(IStorage):
    __data: StorageData
    __db: shelve.Shelf

    @classmethod
    def new(cls, path: Path | str) -> RentalStorage:
        db: shelve.Shelf = shelve.open(path, "n")
        db["data"] = StorageData()
        db.sync()
        return cls(db, cls.__private)

    @classmethod
    def open(cls, path: Path | str) -> RentalStorage:
        db: shelve.Shelf = shelve.open(path, "w")
        return cls(db, cls.__private)

    __private: ClassVar[object] = object() # Hacky guard to prevent others to use this constructor
    def __init__(self, db: shelve.Shelf, private: object) -> None:
        if private is not self.__private:
            raise RentalException("RentalStorage constructor is private")

        self.__db = db
        try:
            self.__data = db["data"]
        except Exception as e:
            raise RentalException("Error loading database") from e

    def close(self) -> None:
        self.__db["data"] = self.__data
        self.__db.sync()
        self.__db.close()

    def get_cars(self) -> Iterable[CarData]:
        return (car for car in self.__data.cars.values())

    def get_car(self, license_plate: LicensePlate) -> CarData:
        if license_plate not in self.__data.cars:
            raise RentalException(f"Car does not exist: {license_plate}")
        return self.__data.cars[license_plate]

    def add_car(self, car: CarData) -> None:
        if not car.license_plate:
            raise RentalException(f"License plate cannot be empty")
        if car.license_plate in self.__data.cars:
            raise RentalException(f"Car already exists: {car.license_plate}")
        self.__data.cars[car.license_plate] = car

    def delete_car(self, license_plate: LicensePlate) -> None:
        if license_plate not in self.__data.cars:
            raise RentalException(f"Car does not exist: {license_plate}")
        del self.__data.cars[license_plate]

    def update_car(self, car: CarData) -> None:
        if car.license_plate not in self.__data.cars:
            raise RentalException(f"Car does not exist: {car.license_plate}")
        self.__data.cars[car.license_plate] = car


    def get_customers(self) -> Iterable[CustomerData]:
        return (customer for customer in self.__data.customers.values())

    def get_customer(self, customer_id: CustomerID) -> CustomerData:
        if customer_id not in self.__data.customers:
            raise RentalException(f"Customer does not exist: {customer_id}")
        return self.__data.customers[customer_id]

    def add_customer(self, customer: CustomerData) -> None:
        if customer.identifier:
            raise RentalException(f"Customer ID cannot be set manually: {customer.identifier}")

        self.__data.customer_id_counter += 1
        customer = CustomerData(
            name=customer.name,
            identifier=self.__data.customer_id_counter
        )
        self.__data.customers[customer.identifier] = customer 

    def delete_customer(self, customer_id: CustomerID) -> None:
        if customer_id not in self.__data.customers:
            raise RentalException(f"Customer does not exist: {customer_id}")
        del self.__data.customers[customer_id]

    def update_customer(self, customer: CustomerData) -> None:
        if customer.identifier not in self.__data.customers:
            raise RentalException(f"Customer does not exist: {customer.identifier}")
        self.__data.customers[customer.identifier] = customer
