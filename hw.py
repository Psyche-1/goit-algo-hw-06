from typing import Callable
from collections import UserDict


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, value: str):
        if len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone must be 10 digit length")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        found_phone = self.find_phone(phone)
        self.phones.remove(found_phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: str):
        for p in self.phones:
            if phone == p.value:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        self.data.pop(name, None)

    def __str__(self):
        return "\n".join(str(self.data[record]) for record in self.data)


def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "User name not found."

    return inner


@input_error
def parse_input(user_input: str):
    """Function parse string to get command and other arguments"""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list[str], contacts: dict[str, str]):
    """Function add phone to contacts by name"""
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]):
    """Function change phone to contacts by name"""
    name, phone = args
    if name not in contacts:
        return f"{name} not found"
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]):
    """Function show phone to contacts by name"""
    name = args[0]
    return contacts[name]


def show_all(contacts: dict[str, str]):
    """Function show all contacts formatted"""
    return "\n".join([f"{contact}: {contacts[contact]}" for contact in contacts])


def main():
    """Function get user input and calls other functions by commands"""
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


def check_work():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі

    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    check_work()
    main()
