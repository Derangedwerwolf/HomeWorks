#from classes import AddressBook
import executionBot


def main():
    """Запускаємо бота"""
    print('Welcome to the adress book')
    
    while True:
        command = input('Please enter your command: ')
        execution = executionBot.data_verification(command)
        
        if execution == 'Exit, bye!':
            quit()
        
        print(execution)
    


if __name__ == '__main__':
    main()