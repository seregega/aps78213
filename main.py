# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    import time
    from aps78213 import Aps78213
    aps = Aps78213("192.168.0.142", 23, 1)
    # aps.connect()
    print(aps.connection_check(), aps.execute_self_test())
    print(aps.meassure_output_vector_dict())
    time.sleep(1)
    # aps.turn_output_on()
    time.sleep(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
