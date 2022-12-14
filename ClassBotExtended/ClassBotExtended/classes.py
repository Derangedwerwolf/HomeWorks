from abc import ABC, abstractmethod
from collections import UserDict
from datetime import date
import pickle
import os
import re

class AddressBook(UserDict):
    N = 0
    cur = 0
    #all_values = []

    def __init__(self):
        super().__init__()
        self.book = []
        
    def save_data(self):
        with open('adress_book.bin', 'wb') as file_in:
            pickle.dump(self.data, file_in)
    
    def unpack_data(self):
        if os.path.exists('adress_book.bin'):
            with open('adress_book.bin', 'rb') as file_out:
                self.data = pickle.load(file_out)
        else:
            self.data = {}
    
    def find_contact(self, name):
        return self.data[name]
    
    def add_record(self, record:object):
        self.data[record.name.value] = record
        
    def iterator(self, number_of_entries):
        self.N += number_of_entries

        for name, phone in self.data.items():
            for value in self.data[name].phones:
                self.book.append(phone.value)
                
    def __next__(self):
        if self.cur < self.N:
            self.cur += 1
            return self.book[self.cur-1]
        else:
            raise StopIteration


class Field(ABC):
    def __init__(self, value=None):
        self._value = value
        #self.value = value
    
    @property
    def value(self):
        return self._value
    

class Name(Field):
    def __repr__(self):
        return f"{self._value}"
    
    @Field.value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    def __repr__(self):
        return f"{''.join(self._value)}"
    
    @Field.value.setter
    def value(self, value):
        #Field.__value = value
        
        if value[0].isnumeric():
            if not value.startswith('+38'):
                value = '+38' + value
            if len(value) != 13:
                pass
            self._value = value
        else:
            print('OOPS')
            raise ValueError


class Birthday(Field):
    def __repr__(self):
        return f"{self._value.strftime('%A %d %B %Y')}"
    
    @Field.value.setter
    def value(self, value):
        if value:
            day, month, year = value.split('.')
            users_birthday = date(day=int(day), month=int(month), year=int(year))
            
            if users_birthday > date.today():
                raise ValueError(f' {users_birthday} Invalid birtday data')
            else:
                self._value = users_birthday
            
    
class Email(Field):
    def __repr__(self) -> str:
        return f"{self._value}"

    @Field.value.setter
    def value(self, value):
        if re.match(r"[a-zA-Z_+-]+\S{1,}\@[a-zA-Z_+-]+\.[a-zA-Z_+-]{2,}", value).group():
            self._value = value
        else:
            raise ValueError(f' {value} Invalid e-mail')


class Note(Field):
    pass
    # def __init__(self, value):
    #     super().__init__()

class Address(Field):
    pass
    # def __init__(self, value):
    #     super().__init__()
        

class Record:
    def __init__(self, name: 'Name', phone: 'Phone' = None, birthday: 'Birthday' = 'birthday', note: 'Note' = 'empty note' , email: 'Email' = 'no email', address: 'Address' = 'no address', ):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        self.note = note
        self.email = email
        self.address = address
        self.tag = {}
        
        if phone:
            self.add_phone(phone)
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        for class_phone in self.phones:
            if class_phone.value == phone.value:
                self.phones.remove(class_phone)
        
    def change(self, phone):
        self.remove_phone(Phone(phone[0]))
        self.add_phone(phone[1])
        
    def add_birthday(self, date):
        self.birthday = Birthday(date)
        
    def days_to_birthday(self):
        self.cur_date = date.today()
        if self.cur_date.month < self.birthday.value.month:
            self.delta_days = date(
                day=int(self.birthday.value.day), month=int(self.birthday.value.month), year=int(self.cur_date.year))
            return (self.delta_days - self.cur_date).days

        else:
            self.delta_days = date(
                day=int(self.birthday.value.day), month=int(self.birthday.value.month), year=int(self.cur_date.year)+1)
            return (self.delta_days - self.cur_date).days
  
    def add_note(self, note):
        self.note =Note(note)
        
    def add_tag(self, tag):
        self.tag["tag"] = tag
        self.tag["note"] = self.note
    
    def add_address(self, address):
        self.address = Address(address)
        
    def delete_address(self):
        self.address = "no address"

    def add_email(self, data):
        self.email = Email(data)
        
    def delete_email(self):
        self.email = "no email"
    
    def __repr__(self):
        return (' , '.join(repr(phone) for phone in self.phones) + ' : ' + repr(self.birthday) + ' : ' + repr(self.email) + ' : ' + repr(self.address) )



