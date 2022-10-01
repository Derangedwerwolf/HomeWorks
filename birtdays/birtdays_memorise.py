from datetime import datetime, timedelta
import calendar
import BIRTHDAY_LIST

def main(users):
    next_week = datetime.today().date() + timedelta(days = 7)
    current_day = datetime.today().date()
    
    if current_day.weekday() == 0 or current_day.weekday() == 1:
        for person_from_users in BIRTHDAY_LIST.users:
            current_day = datetime.today().date() - timedelta(days = 2)
            next_week = datetime.today().date() + timedelta(days = 5)
            
            if person_from_users['birthday'].month >= current_day.month:
                temporal_date = person_from_users['birthday']
                temporal_date = datetime(year=current_day.year, month=temporal_date.month, day=temporal_date.day).date()

            if temporal_date <= next_week:
                
                if temporal_date.weekday() in (5, 6):
                    BIRTHDAY_LIST.weekdays['Monday'] += person_from_users['name']
                
                BIRTHDAY_LIST.weekdays[calendar.day_name[temporal_date.weekday()]].append(person_from_users['name'])
    else:
        for person_from_users in BIRTHDAY_LIST.users:
            
            if person_from_users['birthday'].month >= current_day.month:
                temporal_date = person_from_users['birthday']
                temporal_date = datetime(year=current_day.year, month=temporal_date.month, day=temporal_date.day).date()

                
                BIRTHDAY_LIST.weekdays[calendar.day_name[temporal_date.weekday()]].append(person_from_users['name'])

    for step, name in BIRTHDAY_LIST.weekdays.items():
        print(f'{step}: {", ".join(name)}')

if __name__ == '__main__':
    exit(main(BIRTHDAY_LIST.users))
