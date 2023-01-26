import telnetlib
from time import sleep
from typing import List, Dict, Any


class Aps78213(telnetlib.Telnet, object):
    """
    Class to manage a Command Line Interface connection via Telnet
    """

    measure_vector_name_mask = [
        "Voltage U [V]", "Current I [A]", "Active power P[W]", "Apparent power S[VA]", "Reactive power Q[VAR]",
        "Power factor [cos(phi)]", "Phase difference Φ [DEG]", "Voltage frequency [VHz]", "Current frequency [AHz]",
        "Maximum voltage: U+pk", "Minimum voltage: U-pk", "Maximum current: I+pk", "Minimum current: I-pk",
        "Integration time [s]", "Watt hour WP", "Positive watt hour WP+", "Positive watt hour WP-", "Ampere hour q",
        "Positive ampere hour q+", "Positive ampere hour q", "Maximum power: P+pk", "Minimum power: P-pk",
        "Voltage factor λ", "Current factor λ", "Total harmonic distortion voltage",
        "Total harmonic distortion current",
        "Voltage range", "Current range"
    ]
    measure_vector_key_mask = [
        'U',
        'I',
        'P',
        'S',
        'Q',
        'LAMBda',
        'PHI',
        'FU',
        'FI',
        'UPPeak',
        'UMPeak',
        'IPPeak',
        'IMPeak',
        'TIME',
        'WH',
        'WHP',
        'WHM',
        'AH',
        'AHP',
        'AHM',
        'PPPeaK',
        'PMPeaK',
        'CFU',
        'CFI',
        'UTHD',
        'ITHD',
        'URANge',
        'IRANge'
    ]

    def __init__(self, host, port, timeout):
        # super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout  # Timeout for connecting to telnet
        self.isConnected = False
        super(Aps78213, self).__init__(host, port, timeout)
        self.set_input_mode_acdc()
        self.set_input_voltage_range_300v()
        self.set_input_current_auto_mode()
        self.set_harmonic_thd_fundamental()
        self.set_input_filter_on()
        self.set_input_filter_avg_4()
        self.set_measure_vector_lenght_28()
        self.set_standart_measure_vector_order()

        # telnetlib.Telnet.__init__(self)
        # client = telnetlib.Telnet()
        # self.tn = client

        # CONNECT to device via TELNET, catch connection errors.

    def __enter__(self):
        print('Метод __enter__')
        # self.tn.open(self.host, self.port, self.timeout)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Метод __exit__')
        self.turn_output_off()
        sleep(0.5)
        self.close()
        # if self.tn:
        #     self.tn.__exit__(self.tn)

    def __del__(self):
        self.turn_output_off()
        sleep(0.5)
        self.close()
        # self.tn.__del__

    def connection_check(self):
        self.write(b"*IDN?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a == "GWInstek,GPM-78213,GEW882658,V1.08\r\n":
            return True
        else:
            return False

    def execute_self_test(self):
        self.write(b"*TST?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a == "0\n":
            return True
        else:
            return False

    def output_status(self) -> int:
        self.write(b":OUTPut:STATe?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a == "+1\n":
            return 1
        elif a == "+0\n":
            return 0
        else:
            return -1

    def turn_output_on(self):
        self.write(b":OUTPut:STATe ON\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        return None

    def turn_output_off(self):
        self.write(b":OUTPut:STATe off\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        return None

    def meassure_output_voltage(self) -> float:
        self.write(b":MEASure:SCALar:VOLTage:RMS?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a[0] == "+":
            return float(a[1:-1])
        else:
            return -1

    def meassure_output_active_power(self) -> float:
        self.write(b":MEASure:SCALar:POWer:AC:REAL?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a[0] == "+":
            return float(a[1:-1])
        else:
            return -1

    def meassure_output_frequency(self) -> float:
        self.write(b":MEASure:SCALar:FREQuency?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a[0] == "+":
            return float(a[1:-1])
        else:
            return -1

    def meassure_output_current(self) -> float:
        self.write(b":MEASure:SCALar:CURRent:RMS?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        if a[0] == "+":
            return float(a[1:-1])
        else:
            return -1

    def meassure_output_vector_dict(self) -> dict[str | Any, float] | None:
        self.write(b":NUMeric:NORMal:VALue?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii').split(',')
        if a[0][0].isdecimal():
            b = list(map(float, a))
            return dict(zip(self.measure_vector_key_mask, b))
        else:
            return None

    def meassure_output_vector_list(self) -> list[float] | None:
        self.write(b":NUMeric:NORMal:VALue?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii').split(',')
        if a[0][0].isdecimal():
            b = list(map(float, a))
            return b
        else:
            return None

    def meassure_power_vector(self) -> tuple[float, float, float, float, float, float] | int:
        self.write(b":READ?\n")
        # return self.tn.read_until(b"\n", 2).decode('ascii')
        a = self.read_until(b"\n", 2).decode('ascii')
        b = a.replace('+', '').split(',')
        c = list(map(float, b))
        volt = c[0]
        current = c[1]
        freq = c[2]
        power = c[3]
        sva = c[4]
        ipeak = c[5]
        if a[0] == "+":
            return volt, current, freq, power, sva, ipeak
        else:
            return -1

    def set_output_voltage(self, volt: int | float) -> bool:
        if 100 < volt < 310:
            volt = round(volt, 1)
            command = f":VOLT {volt}\n".encode('ascii')
            self.write(command)
            return True
        else:
            return False

    def set_output_frequency(self, freq: int | float) -> bool:
        if 44 < freq < 56:
            freq = round(freq, 1)
            command = f":FREQ {freq}\n".encode('ascii')
            self.write(command)
            return True
        else:
            return False

    def set_current_limit(self, current: int | float) -> bool:
        if 1 < current < 4:
            current = round(current, 1)
            command = f":CURR:LIM:RMS {current}\n".encode('ascii')
            self.write(command)
            return True
        else:
            return False

    def set_voltage_limit(self, volt: int | float) -> bool:
        if 120 < volt < 311:
            volt = round(volt, 1)
            command = f":VOLTage:LIMit:RMS {volt}\n".encode('ascii')
            self.write(command)
            return True
        else:
            return False

    def set_dysplay_mod(self) -> bool:
        command = f":DISP:DES:MODE SIMPle\n".encode('ascii')
        self.write(command)
        return True

    def set_dysp(self) -> bool:
        command = f":DISP:DES:MODE SIMPle\n".encode('ascii')
        self.write(command)
        return True

    def set_input_mode_acdc(self) -> bool:
        command = f":INPut:MODE ACDC\r\n".encode('ascii')
        self.write(command)
        return True

    def set_input_voltage_range_300v(self) -> bool:
        command = f":INPUT:VOLTAGE:RANGE 300V\r\n".encode('ascii')
        self.write(command)
        return True

    def set_input_current_auto_mode(self) -> bool:
        command = f":INPUT:CURRENT:AUTO ON\r\n".encode('ascii')
        self.write(command)
        return True

    def set_input_filter_on(self) -> bool:
        command = f":INPUT:FILTER ON\r\n".encode('ascii')
        self.write(command)
        return True

    def set_input_filter_avg_4(self) -> bool:
        command = f":MEASURE:AVERAGING:COUNT 4\r\n".encode('ascii')
        self.write(command)
        return True

    def set_measure_vector_lenght_28(self) -> bool:
        command = f":NUMERIC:NORMAL:NUMBER 28\r\n".encode('ascii')
        self.write(command)
        return True

    def set_standart_measure_vector_order(self) -> bool:
        command = f":NUMERIC:NORMAL:ITEM1 U\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM2 I\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM3 P\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM4 S\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM5 Q\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM6 LAMBda\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM7 PHI\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM8 FU\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM9 FI\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM10 UPPeak\r\n".encode('ascii')
        self.write(command)

        command = f":NUMERIC:NORMAL:ITEM11 UMPeak\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM12 IPPeak\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM13 IMPeak\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM14 TIME\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM15 WH\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM16 WHP\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM17 WHM\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM18 AH\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM19 AHP\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM20 AHM\r\n".encode('ascii')
        self.write(command)

        command = f":NUMERIC:NORMAL:ITEM21 PPPeaK\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM22 PMPeaK\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM23 CFU\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM24 CFI\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM25 UTHD\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM26 ITHD\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM27 URANge\r\n".encode('ascii')
        self.write(command)
        command = f":NUMERIC:NORMAL:ITEM28 IRANge\r\n".encode('ascii')
        self.write(command)

    def set_harmonic_thd_fundamental(self) -> bool:
        command = f":HARMONICS:THD FUNDAMENTAL\n".encode('ascii')
        self.write(command)
        return True

    def set_turnon_with_power_off(self) -> bool:
        command = f":OUTPut:PON OFF\n".encode('ascii')
        self.write(command)
        return True

    def clear_internal_error(self) -> bool:
        command = f"*CLS\n".encode('ascii')
        self.write(command)
        return True

    def get_printebale_string_w_measures(self):
        a = self.meassure_output_vector_list()
        for i in range(len(a)):
            print(self.measure_vector_name_mask[i], '=', f'{round(a[i], 3)}')

    # def connect(self):
    #     try:
    #         if self.isConnected:
    #             self.close()
    #         print("Connecting...")
    #         self.open(self.host, self.port, self.timeout)
    #         # telnetlib.Telnet.connect(self,)
    #         print("Connection Establised")
    #         self.isConnected = True
    #
    #     except Exception as ex:
    #         print("Connection Failed")
    #         self.isConnected = False

    # def sendCmd(self, cmd):
    #     # CHECK if connected, if not then reconnect
    #     output = {}
    #     # if not self.reconnect():
    #     #     return output
    #
    #     # Ensure cmd is valid, strip out \r\t\n, etc
    #     cmd = self.validateCmd(cmd)
    #
    #     # Send Command and newline
    #     self.tn.write(cmd + "\n")
    #
    #     response = ''
    #     try:
    #         response = self.tn.read_until('\n*', 5)
    #         if len(response) == 0:
    #             print("No data returned!")
    #             self.isConnected = False
    #     except EOFError:
    #         print("Telnet Not Connected!")
    #         self.isConnected = False
    #
    #     output = self.parseCmdStatus(response)
    #
    #     return output
