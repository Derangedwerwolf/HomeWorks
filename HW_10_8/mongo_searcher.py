from pprint import pprint 
from mongoengine import disconnect, dereference
from mongoengine.queryset.visitor import Q

from HW_10_8.models import Authors, Quotes



def search1(name: str):
    exemp_quote = Quotes.objects(author=name).all()
    
    for quotation in exemp_quote:
        pprint(quotation.author)
        pprint(quotation.quote)
    

def search2(tag: str):
    result = Quotes.objects(tags__contains=tag).all()
    
    for res in result:
        pprint(res.author)
        pprint(res.quote)


def search3(tag: str, tag2: str):
    result = Quotes.objects(Q(tags__contains=tag) | Q(tags__contains=tag2)).all()
    
    for res in result:
        pprint(res.author)
        pprint(res.quote)



if __name__ == '__main__':
    #search1(name)
    #search2(tag)
    #search3(tag, tag2)
    ...
