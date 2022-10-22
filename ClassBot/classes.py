from collections import UserDict

class AddressBook(UserDict):
    def find_contact(self, name):
        return self.data[name]
    
    def add_record(self, record:object):
        self.data[record.name.value] = record

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def add(self, phone):
        self.phones.append(Phone(phone))
    
    def remove(self, phone):
        self.phones.remove(Phone(phone))
    
    def change(self, old_phone, new_phone):
        self.remove(Phone(old_phone))
        self.add(Phone(new_phone))
        
    def __repr__(self):
        return ' , '.join(repr(phone) for phone in self.phones)


class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    def __repr__(self):
        return f"{self.value}"
    pass

class Phone(Field):
    def __repr__(self):
        return f"{self.value}"
    pass
