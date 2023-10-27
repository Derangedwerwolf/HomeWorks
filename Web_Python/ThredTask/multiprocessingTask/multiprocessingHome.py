from multiprocessing import cpu_count, Pool, current_process
#from time import time
import logging
import timeit

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize(*numbers) -> list[list[int]]:
    result = []
    
    for num in numbers:
        new_numbers = []
        operand = 1
        
        logger.debug(f'St:  {current_process().name}')  
        
        while operand <= num:
            if num % operand != 0:
                operand += 1
                continue
            new_numbers.append(operand)
            operand += 1
            
        result.append(new_numbers)
        
    return result


if __name__ == '__main__':
    starttime = timeit.default_timer()
    
    with Pool(8) as pool:
        pool.map(factorize, (128, 255, 99999, 10651060))
        # Устаревшая форма передачи аргументов функции в разных процессах
        # pool.apply(factorize, (128, 255, 99999, 10651060))

    logger.debug(f'Starting: {current_process().name}')    
        
    print(f'Working time: {timeit.default_timer() - starttime}')
    print(f'CPU - {cpu_count()}')



