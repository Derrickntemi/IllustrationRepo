import logging

# get logger incase of several instances of logging, creating a Logging mixin would be preferable,for instance;

# class LoggerMixin(object):
#     @property
#     def logger(self):
#         name = '.'.join([
#             self.__module__,
#             self.__class__.__name__
#         ])
#         return logging.getLogger(name)

# inherit this class to get instance of logger

logger = logging.getLogger(__name__)
# set the logger level
logger.setLevel(logging.INFO)
# format of the log message
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# add a file handler for the logging, a file by the name employee.log gets created| can also use a stream handler
# mode 'a' to append log messages to file
file_handler = logging.FileHandler('employee.log', 'a')
# set format of the message to the file file_handler
file_handler.setFormatter(formatter)
# add handler to logger
logger.addHandler(file_handler)


class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last
        # logging to the file
        logger.info(f'Created Employee: {self.fullname} - {self.email}')
    # decorator, route to __getattr__, encapsulation
    @property
    def email(self):
        return f'{self.first}.{self.last}@email.com'
    # decorator, route to __getattr__, encapsulation
    @property
    def fullname(self):
        return f'{self.first} {self.last}'


emp_1 = Employee('Derrick', 'Kimathi')
emp_2 = Employee('Brandon', 'mawira')
emp_3 = Employee('Doris', 'chamba')
