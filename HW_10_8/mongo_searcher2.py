from pprint import pprint
import json
from mongoengine import disconnect, dereference
from mongoengine.queryset.visitor import Q

from HW_10_8.models import Authors, Quotes
from HW_10_8.connector import redis_client, cache_prefix



#def redis_cache_wrapper(expiration_time=3600):
    
def decorator_cache(redis_func):
    
    def wrapper(*args, **kwargs):
        cache_key = f"{cache_prefix}:{redis_func.__name__}:{args}:{kwargs}"

        if redis_client.exists(cache_key):
            print("Cache hit")
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                cached_json = json.loads(cached_data)
                for item in cached_json:
                    cached_dict = json.loads(item)
                    pprint(cached_dict)
                return cached_json
            
        data = redis_func(*args, **kwargs)
        #print(data)

        if data is not None:
            redis_client.set(cache_key, json.dumps(data), ex=3600)
            pprint("Cached")
            pprint(data)
            # json_data = [json.loads(quote) for quote in data]
            # redis_client.set(cache_key, json.dumps(json_data), ex=3600)

        
        return data
    
    return wrapper
    
    #return decorator_cache



#@redis_cache_wrapper
@decorator_cache
def search1(name: str):
    exemp_quote = Quotes.objects(author=name).all()

    # for quotation in exemp_quote:
    #     pprint(quotation.author)
    #     pprint(quotation.quote)
    
    result = [quotation.to_json() for quotation in exemp_quote]

    return result


#@redis_cache_wrapper
@decorator_cache
def search2(tag: str):
    results = Quotes.objects(tags__contains=tag).all()
    
    # for res in result:
    #     pprint(res.author)
    #     pprint(res.quote)
    
    end_result = [result.to_json() for result in results]
    
    return end_result


#@decorator_cache
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
        
    
#disconnect()


    # author = Authors.objects(fullname__contains=(name)).first()
    
    # if author:
    #     quotes = Quotes.objects(author_ref=author.id).first()
        
    #     pprint(quotes.tags)