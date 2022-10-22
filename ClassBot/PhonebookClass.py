from classes import AddressBook, Record

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
        except AttributeError: 
            return "'NoneType' object has no attribute 'isnumeric'"
    
    return cheker


def hello_handler():
    return 'How can I help you'

@input_error
def add_contact(data):
    """Заповнюємо записну книжку"""
    name, phone = data_splitter(data)
    new_record = Record(name)
    new_record.add(phone)
    
    users_book.add_record(new_record)
    return 'New contact added'

@input_error
def change_contact(data):
    """Змінюємо контактні данні"""
    name, phone = data_splitter(data)
    
    users_book.data[name.casefold()] = phone
    return 'Contact changed'

@input_error
def add_new_phone(data):
    """Додаємо телефонний номер до вже створенного контакту"""
    name, phone = data_splitter(data)
    record_add_phone = users_book.data[name]
    record_add_phone.add(phone)
    return f'A new phone: {phone}, has been added to contact name: {name}.'

@input_error
def delete_func(data):
    """Видаляємо контак із записної книжки із телефоном(нами)"""
    name, phone = data_splitter(data)
    record_delete = users_book.data[name]

    if record_delete.remove(phone) is True:
        return f'Contact name: {name} phone: {phone}, has been deleted.'

    else:
        return 'The phone number not exist'
    
@input_error
def show_name(name):
    if name.strip() not in users_book:
        return 'This contact does not exist.'
    return users_book.data[name.casefold()]

def show_all():
    return users_book

def exit_handler():
    return 'Exit, bye!'

COMMANDS_LIST = {
    'hello' : hello_handler,
    'add' : add_contact,
    'add_phone': add_new_phone,
    'delete': delete_func,
    'change' : change_contact,
    'phone' : show_name,
    'show all' : show_all,
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
    else:
        command, accompanying_data = command.split(' ', maxsplit=1)
        return COMMANDS_LIST[command.casefold()](accompanying_data.casefold())
        

def main():
    """Запускаємо бота"""
    print('Welcome to the adress book')
    
    while True:
        command = input('Please enter your command: ')
        execution = data_verification(command)
        
        if execution == 'Exit, bye!':
            quit()
        
        print(execution)


if __name__ == '__main__':
    users_book = AddressBook()
    main()
