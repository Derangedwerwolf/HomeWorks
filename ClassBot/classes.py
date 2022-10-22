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
            self.add(phone)
    
    def add(self, phone):
        self.phones.append(Phone(phone))
    
    def remove(self, phone):
        for class_phone in self.phones:
            if class_phone.value == phone:
                self.phones.remove(class_phone)
    
    def change(self, old_phone, new_phone):
        self.remove(old_phone)
        self.add(new_phone))
        
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
