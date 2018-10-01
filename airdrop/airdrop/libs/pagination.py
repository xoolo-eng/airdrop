from django.conf import settings


def count_pages(count):
    result = count / settings.COUTN_ITEMS
    test = int(result)
    if result > test:
        return test + 1
    else:
        return test


def pages(num):
    return (
        (num - 1) * settings.COUTN_ITEMS,
        ((num - 1) * settings.COUTN_ITEMS) + settings.COUTN_ITEMS
    )
