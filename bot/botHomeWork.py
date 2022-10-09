PHONE_BOOK = {}

def input_error(func):
    """Перевіряємо на помилки"""
    
    def cheker(*args):
        try:
            return func(*args)
        except KeyError:
            return 'Unidentified request'
        except ValueError:
            return 'Unexpected incoming data.'
        except IndexError:
            return 'Not found'
        except UnboundLocalError:
            return 'Not enough input data.'
    
    return cheker


def hello_handler():
    return 'How can I help you'

@input_error
def add_contact(data):
    """Заповнюємо записну книжку"""
    name, phone = data_splitter(data)
    
    #name, phone = input('Enter name and a phone: ').split()
    PHONE_BOOK[name.casefold()] = phone
    return 'New contact added'

@input_error
def change_contact(data):
    """Змінюємо контактні данні"""
    name, phone = data_splitter(data)
    
    #name, phone = [name_in_book for name_in_book in input("Enter name and a new phone: ").split()]
    PHONE_BOOK[name.casefold()] = phone
    return 'Contact changed'
    
@input_error
def show_name(name):
    #name = input('Enter name: ')
    if name.strip() not in PHONE_BOOK:
        return 'This contact does not exist.'
    return PHONE_BOOK[name.casefold()]


def show_all():
    return PHONE_BOOK
    

def exit_handler():
    return 'Exit, bye!'
    

commands_list = {
    'hello' : hello_handler,
    'add' : add_contact,
    'change' : change_contact,
    'phone' : show_name,
    'show all' : show_all,
    'good bye' : exit_handler,
    'close' : exit_handler,
    'exit' : exit_handler
}

@input_error
def data_splitter(data):
    name, phone = data.split()
<<<<<<< Updated upstream
=======
        
>>>>>>> Stashed changes
    return name, phone

@input_error
def data_verification(command):
    """
    Розбиваємо отриману стрічку на головні частини.
    Після чього перевіряємо валідність команди чи 
    наявність усіх данних.
    """
    
    if command in ('hello', 'show all', 'good bye', 'close', 'exit'):
        return commands_list[command.casefold()]()
    elif len(command.split()) < 2:
        return 'Not enough arguments.'
    else:
        command, accompanying_data = command.split(' ', maxsplit=1)
        return commands_list[command.casefold()](accompanying_data.casefold())
        
        # if command.casefold() not in commands_list:
        #     return 'Command is unrecognised. Please try again.'
        #     #raise KeyError('Command is unrecognised. Please try again.')
        # else:
        #     return commands_list[command.casefold()](accompanying_data.casefold())
    

def main():
    """Запускаємо бота"""
    
    while True:
        command = input('Please enter your command: ')
        execution = data_verification(command)
        
        if execution == 'Exit, bye!':
            quit()
        
        print(execution)


if __name__ == '__main__':
    main()
