from __future__ import annotations
from typing import Protocol, Iterable
from dataclasses import dataclass

from typing import Protocol, Iterable
from dataclasses import dataclass
from .terminal_menu import TerminalMenu, TerminalMenuAction, TerminalUserQuit

from .UILogger import UILogger
from .types import CUSTOMER_ID_UNSET
@dataclass(frozen=True)
class Customer:
    name: str
    identifier: int

@dataclass(frozen=True)
class Car:
    license_plate: str
    manufacturer: str
    model: str
    rented_by_customer: int


class IManager(Protocol):
    def get_cars(self) -> Iterable[Car]: ...
    def get_customers(self) -> Iterable[Customer]: ...
    def rent_car(self, customer_id: int, car_model: str) -> None: ...
    def return_car(self, license_plate: str) -> None: ...
    def add_car(self, license_plate: str, manufacturer: str, model: str) -> None: ...
    def remove_car(self, license_plate: str) -> None: ...
    def add_customer(self, customer_name: str) -> None: ...
    def remove_customer(self, customer_id: int) -> None: ...



class RentalCarUI(TerminalMenu):
    __manager: IManager


    def __init__(self, manager: IManager) -> None:
        # super() ruft jetzt korrekt TerminalMenu.__init__ auf!
        super().__init__("Welcome the Rental Car Manager App",[
            TerminalMenuAction("View...", self.__view_menu),
            TerminalMenuAction("Car...", self.__car_menu),
            TerminalMenuAction("Customer...", self.__customer_menu)
        ])
        self.__manager = manager

    def open(self) -> None:
        try: 
            super().open()
        except TerminalUserQuit: 
            pass

    # --- VIEW MENU ---
    def __view_menu(self) -> None:
        TerminalMenu("View...",[
            TerminalMenuAction("All cars", self.__view_all_cars),
            TerminalMenuAction("All customers", self.__view_all_customers),
            TerminalMenuAction("Available car models", self.__view_available_car_models),
        ]).open()

    def __view_all_cars(self) -> None:
        print(*self.__manager.get_cars(), sep="\n")

    def __view_all_customers(self) -> None:
        print(*self.__manager.get_customers(), sep="\n")

    def __view_available_car_models(self) -> None:
        models: set[str] = {
            f"{car.manufacturer} {car.model}"
            for car in self.__manager.get_cars()
            if car.rented_by_customer == CUSTOMER_ID_UNSET  
        }
        print(*models, sep="\n")

    # --- CAR MENU ---
    def __car_menu(self) -> None:
        TerminalMenu("Car Menu",[
            TerminalMenuAction("Rent car", self.__rent_car),
            TerminalMenuAction("Return car", self.__return_car),
            TerminalMenuAction("Add car", self.__add_car),
            TerminalMenuAction("Remove car", self.__remove_car)
        ]).open()

    def __rent_car(self) -> None:
        self.__manager.rent_car(self._get_input("Customer ID", int), self._get_input("Car model", str))

    def __return_car(self) -> None:
        self.__manager.return_car(self._get_input("License plate", str))

    def __add_car(self) -> None:
        self.__manager.add_car(
            self._get_input("License plate", str),
            self._get_input("Manufacturer", str),
            self._get_input("Model", str)
        )

    def __remove_car(self) -> None:
        self.__manager.remove_car(self._get_input("License plate", str))

    # --- CUSTOMER MENU ---
    def __customer_menu(self) -> None:
        TerminalMenu("Customer Menu",[
            TerminalMenuAction("Add customer", self.__add_customer),
            TerminalMenuAction("Remove customer", self.__remove_customer)
        ]).open()

    def __add_customer(self) -> None:
        self.__manager.add_customer(self._get_input("Customer name", str))

    def __remove_customer(self) -> None:
        self.__manager.remove_customer(self._get_input("Customer ID", int))
