from django.core.exceptions import ValidationError


# def validate_int15_list(value):
#     """
#         Service time must be a multiplication of 15
#     :param value:
#     :return:
#     """
#     list = value.split(',')
#
#     try:
#         for x in list:
#             v = int(x.strip())
#             if v <= 0 or v % 15 != 0:
#                 raise ValidationError("Some elements are not integer", params={'value': value})
#     except ValueError:
#         raise ValidationError("Some elements are not integer", params={'value': value})

def validate_int15_multipler(value):
    """
        Service time must be a multiplication of 15
    :param value:
    :return:
    """
    try:
        if value % 15 != 0:
            raise ValidationError("value is not a multiplication of 15 ", params={'value': value})
    except ValueError:
        raise ValidationError("value are not integer", params={'value': value})
