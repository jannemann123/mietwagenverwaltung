from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any


from .UILogger import UILogger
from .exceptions import RentalException



class TerminalUserCancelled(Exception): pass
class TerminalUserQuit(Exception): pass


@dataclass(frozen=True)
class TerminalMenuAction:
    name: str
    action: Callable[[], Any]


class TerminalMenu:
    _title: str
    _menu: list[TerminalMenuAction]
    _log: UILogger
    __is_open: bool

    # Some ANSI escape codes
    __BLUE:    str = "\033[1;34m"
    __MAGENTA: str = "\033[1;35m"
    __ESC:     str = "\033[m"

    def __init__(self, title: str, menu: list[TerminalMenuAction]) -> None:
        self._title = title
        self._menu = menu
        self.__is_open = False
        self._log = UILogger("UI")

    def open(self) -> None:
        self.__is_open = True
        while self.__is_open:
            print()
            print(f"{self.__BLUE}{self._title}{self.__ESC}")
            action: Callable[[], Any]
            try: action = self._select()
            except TerminalUserCancelled: break

            try: action()
            except RentalException as e:
                print(e)
                self._log.warning(f"Caught {repr(e)}")
            except TerminalUserCancelled: pass
        self.__is_open = False

    def close(self) -> None:
        self.__is_open = False

    def _get_input[T](self, prompt: str = "", use_type: Callable[[str], T] = str) -> T:
        if prompt: print(prompt + ":")
        inp: T
        while True:
            try: inp = use_type(input(f"{self.__MAGENTA}>>> {self.__ESC}"))
            except KeyboardInterrupt:
                print()
                raise TerminalUserCancelled()
            except EOFError:
                print()
                raise TerminalUserQuit()
            except ValueError: continue
            if not inp: continue
            break
        return inp

    def _select(self) -> Callable[[], Any]:
        for i, option in enumerate(self._menu, start=1):
            print(f"{i}) {option.name}")
        print("Q) Quit")
        print()
        option_num: int
        while True:
            inp: str = self._get_input()
            if not inp or inp.lower() == "q": raise TerminalUserCancelled()
            try: option_num = int(inp) - 1
            except ValueError: continue
            if option_num not in range(len(self._menu)): continue
            break
        return self._menu[option_num].action
