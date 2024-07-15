from abc import ABC, abstractmethod

class UserView(ABC):
    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def show_all(self, data):
        pass

    @abstractmethod
    def show_record(self, record):
        pass

    @abstractmethod
    def show_error(self, error_message):
        pass

    @abstractmethod
    def prompt_user(self, prompt):
        pass

class ConsoleView(UserView):
    def show_message(self, message):
        print(message)

    def show_all(self, data):
        for record in data:
            print(record)

    def show_record(self, record):
        print(record)

    def show_error(self, error_message):
        print(f"Error: {error_message}")

    def prompt_user(self, prompt):
        return input(prompt)
