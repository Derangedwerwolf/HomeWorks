from collections import UserDict

class AddressBook(UserDict):
    def find_contact(self, name):
        return self.data[name]
    
    def add_record(self, record:object):
        self.data[record.name.value] = record

class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        
        if phone:
            self.add_phone(phone)
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        for class_phone in self.phones:
            if class_phone == phone:
                print("DONE")
                self.phones.remove(class_phone)
        
    
    def change(self, *phone):
        self.remove_phone(phone[0])
        self.add_phone(phone[1])
        
    def __repr__(self):
        return ' , '.join(repr(phone) for phone in self.phones)


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __repr__(self):
        return f"{self.value}"
    pass

class Phone(Field):
    def __repr__(self):
        return f"{self.value}"
    pass
