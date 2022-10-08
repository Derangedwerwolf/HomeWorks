PHONE_BOOK = {}

def input_error(func):
    """Перевіряємо на помилки"""
    
    def cheker(*args):
        try:
            result = func(*args)
        except KeyError:
            print('Unidentified request')
        except ValueError:
            print('Unexpected incoming data.')
        except IndexError:
            print('Not found')
        return result
    
    return cheker


def hello_handler():
    return 'How can I help you'

@input_error
def add_contact(name, phone):
    """Заповнюємо записну книжку"""
    
    #name, phone = input('Enter name and a phone: ').split()
    PHONE_BOOK[name.casefold()] = phone
    return 'New contact added'

@input_error
def change_contact(name, phone):
    """Змінюємо контактні данні"""
    
    #name, phone = [name_in_book for name_in_book in input("Enter name and a new phone: ").split()]
    PHONE_BOOK[name.casefold()] = phone
    return 'Contact changed'
    
@input_error
def show_name(name):
    #name = input('Enter name: ')
    return PHONE_BOOK[name.casefold()]


def show_all():
    return PHONE_BOOK
    

def exit_handler():
    print('Exit, bye!')
    quit()
    

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

def data_splitter(command):
    try:
        command, accompanying_data = command.split(' ', maxsplit=1)
        name, phone = accompanying_data.split()
    except ValueError:
        print('Oops, you have, probably, forgot something. Please, try again.')
            
    return command, name, phone

def data_verification(command):
    if command in ('hello', 'show all', 'good bye', 'close', 'exit'):
        return commands_list[command.casefold()]()
    elif len(command.split()) < 2:
        return 'Not enough arguments.'
        #raise UnboundLocalError('Not enough arguments.')
    else:
        command, name, phone = [data for data in (data_splitter(command))]
    
        if command.casefold() not in commands_list:
            return 'Command is unrecognised. Please try again.'
            #raise KeyError('Command is unrecognised. Please try again.')
        else:
            return commands_list[command.casefold()](name, phone)
    

def main():
    """Запускаємо бота"""
    
    while True:
        command = input('Please enter your command: ')
        print(data_verification(command))


if __name__ == '__main__':
    main()
