from classes import Record
import globalVariable


instructions = """
Greeting message: "helo"
Add a new contact: "add"/ contact's name / contacts phone
Change phone for existing contact: "change" / contact's name / new contacts phone
Add new phone for existing contact: "add_phone" / contact's name
Delete the phone for the contact: "delete" / contact's name
Show the contact's phone number: "phone" / contact's name
Add a birthday for a contact: "add_birthday" / contact's name / birthday date (DD.MM.YY)
View all contacts : "show all"
View set number from address book : "desplay" / number of elements
Search by match : "search" / search data

Show this text again : "help"
"""

def input_error(func):
    """Перевіряємо на помилки"""
    
    def cheker(*args):
        try:
            return func(*args)
        except KeyError:
            return 'Unidentified request'
        except TypeError:
            return 'Operation on an object is not supported'
        except ValueError:
            return 'Unexpected incoming data.'
        except IndexError:
            return 'Not found'
        except UnboundLocalError:
            return 'Not enough input data.'

    return cheker


def hello_handler():
    return 'How can I help you'

def get_help():
    return instructions

@input_error
def add_contact(data):
    """Заповнюємо записну книжку (Ім'я, *номер телефону, *день народженя)"""
    name, phone =data_splitter(data)
    new_record = Record(name, phone)
    
    globalVariable.users_book.add_record(new_record)
    return 'New contact added'

@input_error
def change_contact(data):
    """Змінюємо контактні данні"""
    name, *phone = data.split()

    globalVariable.users_book.data[name.casefold()].change(phone)
    return 'Contact changed'

@input_error
def add_new_phone(data):
    """Додаємо телефонний номер до вже створенного контакту"""
    name, phone = data_splitter(data)
    globalVariable.users_book.data[name.casefold()].add_phone(phone)
    return f'A new phone: {phone}, has been added to contact name: {name}.'

@input_error
def delete_func(data):
    """Видаляємо контак із записної книжки із телефоном(нами)"""
    name, phone = data_splitter(data)
    record_delete = globalVariable.users_book.data[name.casefold()]

    if record_delete.remove(phone) is True:
        return f'Contact name: {name} phone: {phone}, has been deleted.'
    else:
        return 'The phone number not exist'
    
@input_error
def show_phone(name):
    if name.strip() not in globalVariable.users_book:
        return 'This contact does not exist.'
    return globalVariable.users_book.data[name.casefold()]

@input_error
def show_name(phone):
    if phone.strip() not in globalVariable.users_book.values():
        return 'This phone does not exist.'
    return globalVariable.users_book.data[phone.casefold()]

@input_error
def show_all():
    return globalVariable.users_book

@input_error
def search(data):
    for users in globalVariable.users_book.values():
        for elem in users.phones.value:
            if data in elem:
                return users
        if data in users.name.value:
            return users

@input_error
def add_birthday(data):
    name, date_of_birthday = data.split()
    print(date_of_birthday)
    globalVariable.users_book.data[name.casefold()].add_birthday(date_of_birthday)
    return 'Birthday added'

@input_error
def days_to_birthday(name):
    return globalVariable.users_book.data[name.casefold()].days_to_birthday()

@input_error
def display(count):
    count = int(count)
    globalVariable.users_book.iteration(count)

    for _ in range(count):
        print(next(globalVariable.users_book))

def save_data():
    globalVariable.users_book.save_data
    return "File successfully saved to 'adress_book.bin'"

def unpack_data():
    globalVariable.users_book.unpack_data
    return "Data unloaded"

def exit_handler():
    return 'Exit, bye!'

COMMANDS_LIST = {
    'hello' : hello_handler,
    'help' : get_help,
    'add' : add_contact,
    'add_phone': add_new_phone,
    'delete': delete_func,
    'change' : change_contact,
    'show_phone' : show_phone,
    'show_name' : show_name,
    'display' : display,
    'show all' : show_all,
    'search': search,
    'add_birthday' : add_birthday,
    'days_to_birthday' : days_to_birthday,
    'save_file' : save_data,
    'load_file' : unpack_data,
    'good bye' : exit_handler,
    'close' : exit_handler,
    'exit' : exit_handler
}

@input_error
def data_splitter(data):
    name, phone = data.split() if len(data.split()) > 1 else [data, None]
    return name, phone

@input_error
def data_verification(command):
    """
    Розбиваємо отриману стрічку на головні частини.
    Після чього перевіряємо валідність команди чи 
    наявність усіх данних.
    """
    
    if command in ('hello', 'show all', 'good bye', 'close', 'exit'):
        return COMMANDS_LIST[command.casefold()]()
    elif command == 'display':
        command, count = command.split(' ', maxsplit=1)
        return COMMANDS_LIST[command.casefold()](count())
    else:
        if len(command.split()) < 2:
            command = command
            print(command)
            return COMMANDS_LIST[command.casefold()]()
        else:
            command, accompanying_data = command.split(' ', maxsplit=1)
        print(command)
        return COMMANDS_LIST[command.casefold()](accompanying_data.casefold())

