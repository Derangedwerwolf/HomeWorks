PHONE_BOOK = {}

def input_error(func):
    """Перевіряємо на помилки"""
    
    def cheker(indicator):
        try:
            func()
        except KeyError:
            print('Unidentified request')
        except ValueError:
            print('Unexpected incoming data.')
        except IndexError:
            print('Not found')
    
    return cheker


def hello_handler():
    print('How can I help you')

@input_error
def add_contact(name, phone):
    """Заповнюємо записну книжку"""
    
    name, phone = input('Enter name and a phone: ').split()
    PHONE_BOOK[name.casefold()] = phone
    print('New contact added')

@input_error
def change_contact(name, phone):
    """Змінюємо контактні данні"""
    
    name, phone = [name_in_book for name_in_book in input("Enter name and a new phone: ").split()]
    PHONE_BOOK[name.casefold()] = phone
    
@input_error
def show_name(name):
    name = input('Enter name: ')
    print(PHONE_BOOK[name.casefold()])


def show_all():
    print(PHONE_BOOK)
    

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


def main():
    """Запускаємо бота"""
    
    while True:
        command = input('Please enter your command: ')
        if command.casefold() not in commands_list:
            print('Command is unrecognised. Please try again.')
            continue
        else:
            commands_list[command.casefold()]()


if __name__ == '__main__':
    main()
