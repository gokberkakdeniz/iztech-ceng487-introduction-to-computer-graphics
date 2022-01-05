# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np

message_type_of = "The '{name}' must be one of the types: {class_names}"
message_one_of = "The '{name}' must be one of the values: {values}"
message_number = "The '{name}' must be number."


def type_of(o: object,
            name: str,
            types: list,
            message: str = message_type_of):
    if not type(o) in types:
        class_names = ", ".join(map(lambda cls: cls.__name__, types))

        raise TypeError(message.format(name=name, class_names=class_names))


def one_of(o: object,
           name: str,
           values: list,
           message: str = message_one_of):
    if not o in values:
        raise TypeError(message.format(name=name, values=values))


def number(o: object, name: str, message: str = message_number):
    type_of(o, name, [float, int, np.short, np.float, np.double, np.longdouble], message)
