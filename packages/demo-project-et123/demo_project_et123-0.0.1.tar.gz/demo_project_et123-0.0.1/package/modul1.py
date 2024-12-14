# Modul 1
try:
    from . import modul2
except ImportError:
    import modul2


def funktion_1():
    print("Grüße aus Modul 1")
