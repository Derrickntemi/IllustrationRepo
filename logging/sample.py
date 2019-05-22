import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# format for display of log messages
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# mode 'a' so as to avoid overwriting of previously logged messages)
file_handler = logging.FileHandler('sample.log', mode='a')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# add handler for both logger handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def add(x, y):
    return x + y
    
def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        # similar to logger.error
        logger.exception('Tried to divide by zero')
    else:
        return result


num_1 = 10
num_2 = 0

add_result = add(num_1, num_2)
# used f strings for formatting strings
logger.debug(f'Add: {num_1} * {num_2} = {add_result}.')
sub_result = subtract(num_1, num_2)
logger.debug(f'Sub: {num_1} * {num_2} = {sub_result}.')
mul_result = multiply(num_1, num_2)
logger.debug(f'Mul: {num_1} * {num_2} = {mul_result}.')
div_result = divide(num_1, num_2)
logger.debug(f'Div: {num_1} * {num_2} = {div_result}.')
