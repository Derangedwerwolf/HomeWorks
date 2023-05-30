from mongoengine import disconnect

enter_data = input('please choose from: \n\t\t0)Exit\n\t\t1)Save\n\t\t2)Search  ')


if enter_data == '2':
    from HW_10_8.mongo_searcher import *
    
    while True:
        print("Please enter your command:\n\t\
                  0)Exit\n\t\
                  1)Finde all quotes of an aouther\n\t\
                  2)Find all quotes by one tag\n\t\
                  3)Find all quotes by many tags")
        
        number = input()
            
        try:
            match number:
                case '0':
                    exit(0)
                case '1':
                    search1('Steve Martin')
                case '2':
                    search2('life')
                case '3':
                    search3('life', 'live')
                case _:
                    pprint('Unknown command!')
        except ValueError as err:
            pprint(err)

    
elif enter_data =='1':
    from HW_10_8.mongoEngine_loader import *
    
    main()
    
else:
    disconnect()
    exit()
    
#disconnect()