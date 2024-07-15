import pickle
from pathlib import Path
from models import AddressBook, Record
from views import ConsoleView

file_path = Path("database.bin")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Name not found. Please, check and try again."
        except ValueError as e:
            return e
        except IndexError:
            return "Enter correct information."

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book):
    (name,) = args
    record = book.find(name)
    if record:
        return "; ".join([str(phone) for phone in record.phones])
    else:
        raise KeyError

def show_all(book, view):
    view.show_all(book.data.values())

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args, book):
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book):
    (name,) = args
    record = book.find(name)
    return str(record.birthday)

def load_data():
    if file_path.is_file():
        with open(file_path, "rb") as file:
            return pickle.load(file)
    else:
        return AddressBook()

def main():
    book = load_data()
    view = ConsoleView()
    view.show_message("Welcome to the assistant bot!")

    while True:
        user_input = view.prompt_user("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            view.show_message("Good bye!")
            with open(file_path, "wb") as file:
                pickle.dump(book, file)
            break

        elif command == "hello":
            view.show_message("How can I help you?")

        elif command == "add":
            result = add_contact(args, book)
            if isinstance(result, str):
                view.show_message(result)
            else:
                view.show_error(result)

        elif command == "change":
            result = change_contact(args, book)
            if isinstance(result, str):
                view.show_message(result)
            else:
                view.show_error(result)

        elif command == "phone":
            result = show_phone(args, book)
            if isinstance(result, str):
                view.show_message(result)
            else:
                view.show_error(result)

        elif command == "all":
            show_all(book, view)

        elif command == "add-birthday":
            result = add_birthday(args, book)
            if isinstance(result, str):
                view.show_message(result)
            else:
                view.show_error(result)

        elif command == "show-birthday":
            result = show_birthday(args, book)
            if isinstance(result, str):
                view.show_message(result)
            else:
                view.show_error(result)

        elif command == "birthdays":
            birthdays = book.get_upcoming_birthdays()
            if not len(birthdays):
                view.show_message("There are no upcoming birthdays.")
                continue
            for day in birthdays:
                view.show_message(f"{day}")

        else:
            view.show_message("Invalid command.")

if __name__ == "__main__":
    main()
