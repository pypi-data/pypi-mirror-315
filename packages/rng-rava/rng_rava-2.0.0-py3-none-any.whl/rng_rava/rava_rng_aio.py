"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
The RAVA_RNG_AIO class offers the same functionality as RAVA_RNG but within an
asynchronous framework.
"""

import asyncio
import numpy as np

from rng_rava import __version__ as rng_rava_version
from rng_rava import RAVA_RNG
from rng_rava import find_rava_port, version_a_greater_b, print_health_startup_results, bytes_to_list, bytes_to_array
from rng_rava.rava_defs import *


### RAVA_RNG_AIO

class RAVA_RNG_AIO(RAVA_RNG):

    def __init__(self):
        super().__init__(dev_name='RAVA_AIO')
        self.queue_type = asyncio.Queue

        # Variables
        self.serial_listen_task = None


    async def connect(self, serial_number):
        # Debug
        self.lg.debug('> {} CONNECT'.format(self.dev_name))

        # Find serial port
        port = find_rava_port(serial_number)
        if port is None:
            self.lg.error('{} Connect: No device found with SN {}'.format(self.dev_name, serial_number))
            return False

        # Open serial connection
        if not self.open_serial(port):
            return False

        # Reset serial data queues
        self.init_queue_data()

        # Start listening for serial commands
        self.serial_listen_task = asyncio.create_task(self.loop_serial_listen())

        # Stop any active RNG byte stream
        self.snd_rng_byte_stream_stop()

        # Request firmware info
        self.firmware_dict = await self.get_eeprom_firmware()
        self.firmware_version =  self.firmware_dict['version']
        self.health_startup_enabled = self.firmware_dict['health_startup_enabled']
        self.health_continuous_enabled = self.firmware_dict['health_continuous_enabled']
        self.led_enabled = self.firmware_dict['led_enabled']
        self.lamp_enabled = self.firmware_dict['lamp_enabled']
        self.peripherals_enabled = self.firmware_dict['peripherals_enabled']

        # Check Firmware version
        if version_a_greater_b(FIRMWARE_MIN_VERSION, self.firmware_version):
            self.lg.error('{} Connect: Firmware version v{} is incompatible with driver v{}'.format(self.dev_name, self.firmware_version, rng_rava_version))
            self.close()
            return False

        # Print connection info
        self.lg.info('{} Connect: Success'
                '\n{}  SN={} at {}'
                '\n{}  Firmware v{},  Driver v{}'
                .format(self.dev_name,
                        LOG_FILL, self.dev_serial_number, self.serial.port,
                        LOG_FILL, self.firmware_version, rng_rava_version))

        # Request Health startup info
        if self.health_startup_enabled:
            self.health_startup_success, test_vars = await self.get_health_startup_results()

            # Print test info
            print_health_startup_results(self.health_startup_success, test_vars)

            # Error? Users have then a limited command variety (see Firmware code)
            if not self.health_startup_success:
                self.lg.error('{} Connect: Startup tests failed'.format(self.dev_name))
                return False

        # Reset Health continuous erros
        self.get_health_continuous_errors()

        return True


    ## QUEUE

    def put_queue_data(self, comm, value, comm_ext_id=0):
        # Check key
        if comm not in self.serial_data:
            self.lg.error('{} Data: Unknown comm {}'.format(self.dev_name, comm))
            return False

        # Extended key
        if comm_ext_id:
            comm_ext = '{}_{}'.format(comm, comm_ext_id)

            # Queue exists?
            if comm_ext not in self.serial_data:
                self.serial_data[comm_ext] = self.queue_type()
        else:
            comm_ext = comm

        # Try writing to queue
        try:
            self.serial_data[comm_ext].put_nowait(value)
            return True

        except asyncio.QueueFull:
            self.lg.error('{} Data: {} Queue full'.format(self.dev_name, comm_ext))
            return False


    async def get_queue_data(self, comm, comm_ext_id=0):
        # Check key
        if comm not in self.serial_data:
            self.lg.error('{} Data: Unknown comm {}'.format(self.dev_name, comm))
            return None

        # Extended key
        if comm_ext_id:
            comm_ext = '{}_{}'.format(comm, comm_ext_id)

            # Queue exists?
            if comm_ext not in self.serial_data:
                self.serial_data[comm_ext] = self.queue_type()
        else:
            comm_ext = comm

        # Read asyncio queue
        return await self.serial_data[comm_ext].get()


    ## SERIAL

    async def loop_serial_listen(self):
        # Debug
        self.lg.debug('> {} LOOP SERIAL LISTEN'.format(self.dev_name))

        # Loop while connected
        while self.serial_connected.is_set():

            # Command available?
            comm_inwaiting = self.inwaiting_serial()
            if comm_inwaiting is None:
                continue # Disconnected

            if comm_inwaiting > 0:

                # Read command starting char
                comm_start = self.read_serial(1)
                if comm_start is None:
                    continue # Disconnected

                # Starts with $?
                if comm_start == COMM_MSG_START:

                    # Read remaining command bytes
                    comm_msg = self.read_serial(COMM_MSG_LEN-1)
                    if comm_msg is None:
                        continue # Disconnected

                    comm_id = comm_msg[0]
                    comm_data = comm_msg[1:]

                    # Known command id?
                    if comm_id in D_DEV_COMM_INV:

                        # Debug
                        self.lg.debug('> COMM RCV {}'.format([D_DEV_COMM_INV[comm_id], *[c for c in comm_data]]))

                        # Process Command
                        try:
                            self.process_serial_comm(comm_id, comm_data)

                        except Exception as err:
                            self.lg.error('{} Serial Listen Loop: Error processing command_id {}'
                                        '\n{}  {} - {}'
                                        .format(self.dev_name, comm_id, LOG_FILL, type(err).__name__, err))

                            # Close device
                            self.close()

                    else:
                        self.lg.warning('{} Serial Listen Loop: Unknown command_id {}'.format(self.dev_name, comm_id))

                else:
                    self.lg.warning('{} Serial Listen Loop: Commands must start with {}'.format(self.dev_name, COMM_MSG_START))

            # The non-blocking method is prefered for finishing the thread
            # when closing the device
            else:
                await asyncio.sleep(SERIAL_LISTEN_LOOP_INTERVAL_S)


    ## DEVICE

    async def get_device_serial_number(self):
        comm = 'DEVICE_SERIAL_NUMBER'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)


    async def get_device_free_ram(self):
        comm = 'DEVICE_FREE_RAM'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)


    ## EEPROM

    async def get_eeprom_firmware(self):
        comm = 'EEPROM_FIRMWARE'
        if self.snd_rava_msg(comm):
            version_major, version_minor, version_patch, modules = await self.get_queue_data(comm)

            version = '{}.{}.{}'.format(version_major, version_minor, version_patch)
            health_startup_enabled = modules & 1 << 0 != 0
            health_continuous_enabled = modules & 1 << 1 != 0
            led_enabled = modules & 1 << 2 != 0
            lamp_enabled = modules & 1 << 3 != 0
            peripherals_enabled = modules & 1 << 4 != 0
            serial1_enabled = modules & 1 << 5 != 0
            return {'version':version,
                    'health_startup_enabled':health_startup_enabled,
                    'health_continuous_enabled':health_continuous_enabled,
                    'led_enabled':led_enabled,
                    'lamp_enabled':lamp_enabled,
                    'peripherals_enabled':peripherals_enabled,
                    'serial1_enabled':serial1_enabled
                    }


    async def get_eeprom_pwm_boost(self):
        comm = 'EEPROM_PWM_BOOST'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = await self.get_queue_data(comm)
            return {'freq_id':freq_id, 'freq_str':D_PWM_BOOST_FREQ_INV[freq_id], 'duty':duty}


    async def get_eeprom_rng(self):
        comm = 'EEPROM_RNG'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = await self.get_queue_data(comm)
            return {'sampling_interval_us':sampling_interval_us}


    async def get_eeprom_led(self):
        comm = 'EEPROM_LED'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            led_n = await self.get_queue_data(comm)
            return {'led_n':led_n}


    async def get_eeprom_lamp(self):
        comm = 'EEPROM_LAMP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            data_vars = await self.get_queue_data(comm)
            data_names = ['exp_movwin_n_trials', 'exp_deltahits_sigevt', 'exp_dur_max_s', 'exp_mag_smooth_n_trials', 'exp_mag_colorchg_thld', 'sound_volume']
            return dict(zip(data_names, data_vars))


    ## PWM

    async def get_pwm_boost_setup(self):
        rava_send = True
        comm = 'PWM_BOOST_SETUP'
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = await self.get_queue_data(comm)
            return {'freq_id':freq_id, 'freq_str':D_PWM_BOOST_FREQ_INV[freq_id], 'duty':duty}


    ## RNG

    async def get_rng_setup(self):
        comm = 'RNG_SETUP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = await self.get_queue_data(comm)
            return {'sampling_interval_us':sampling_interval_us}


    async def get_rng_pulse_counts(self, n_counts, output_type='array'):
        if n_counts == 0:
            self.lg.error('{} RNG PC: Provide n_counts > 0'.format(self.dev_name))
            return None, None
        if n_counts >= 2**16:
            self.lg.error('{} RNG PC: Provide n_counts as a 16-bit integer'.format(self.dev_name))
            return None, None

        comm = 'RNG_PULSE_COUNTS'
        if self.snd_rava_msg(comm, [n_counts], 'H'):
            counts_bytes_a, counts_bytes_b = await self.get_queue_data(comm)

            if (counts_bytes_a is None) or (counts_bytes_a is None):
                return None, None

            else:
                if output_type == 'list':
                    counts_a = bytes_to_list(counts_bytes_a, 'B')
                    counts_b = bytes_to_list(counts_bytes_b, 'B')
                    return counts_a, counts_b

                elif output_type == 'array':
                    counts_a = bytes_to_array(counts_bytes_a, np.uint8)
                    counts_b = bytes_to_array(counts_bytes_b, np.uint8)
                    return counts_a, counts_b

                else:
                    return counts_bytes_a, counts_bytes_b


    async def get_rng_bits(self, bit_source_id):
        if bit_source_id not in D_RNG_BIT_SRC_INV:
            self.lg.error('{} RNG Bits: Unknown bit_source_id {}'.format(self.dev_name, bit_source_id))
            return None

        comm = 'RNG_BITS'
        if self.snd_rava_msg(comm, [bit_source_id], 'B'):
            bit_source_id_recv, *bits = await self.get_queue_data(comm)

            if bit_source_id == D_RNG_BIT_SRC['AB_RND']:
                bit_type_str = D_RNG_BIT_SRC_INV[bit_source_id_recv]
                return [bit_type_str, bits[0]]
            elif bit_source_id == D_RNG_BIT_SRC['AB']:
                return list(bits)
            else:
                return bits[0]


    async def get_rng_bytes(self, n_bytes, postproc_id=D_RNG_POSTPROC['NONE'], request_id=0, output_type='array'):
        if n_bytes == 0:
            self.lg.error('{} RNG Bytes: Provide n_bytes > 0'.format(self.dev_name))
            return None, None
        if n_bytes >= 2**16:
            self.lg.error('{} RNG Bytes: Provide n_bytes as a 16-bit integer'.format(self.dev_name))
            return None, None
        if postproc_id not in D_RNG_POSTPROC_INV:
            self.lg.error('{} RNG Bytes: Unknown postproc_id {}'.format(self.dev_name, postproc_id))
            return None, None

        comm = 'RNG_BYTES'
        if self.snd_rava_msg(comm, [n_bytes, postproc_id, request_id], 'HBB'):
            rng_bytes_a, rng_bytes_b = await self.get_queue_data(comm, comm_ext_id=request_id)

            if (rng_bytes_a is None) or (rng_bytes_b is None):
                return None, None

            else:
                if output_type == 'list':
                    rng_a = bytes_to_list(rng_bytes_a, 'B')
                    rng_b = bytes_to_list(rng_bytes_b, 'B')
                    return rng_a, rng_b

                elif output_type == 'array':
                    rng_a = bytes_to_array(rng_bytes_a, np.uint8)
                    rng_b = bytes_to_array(rng_bytes_b, np.uint8)
                    return rng_a, rng_b

                else:
                    return rng_bytes_a, rng_bytes_b


    async def get_rng_int8s(self, n_ints, int_delta, output_type='array'):
        if n_ints == 0:
            self.lg.error('{} RNG Ints: Provide n_ints > 0'.format(self.dev_name))
            return None
        if n_ints >= 2**16:
            self.lg.error('{} RNG Ints: Provide n_ints as a 16-bit integer'.format(self.dev_name))
            return None
        if int_delta >= 2**8:
            self.lg.error('{} RNG Ints: Provide int_delta as a 8-bit integer'.format(self.dev_name))
            return None
        if int_delta == 0:
            self.lg.error('{} RNG Ints: Provide int_delta > 0'.format(self.dev_name))
            return None

        comm = 'RNG_INT8S'
        if self.snd_rava_msg(comm, [n_ints, int_delta], 'HB'):
            ints_bytes = await self.get_queue_data(comm)
            if ints_bytes is None:
                return None
            else:
                if output_type == 'list':
                    return bytes_to_list(ints_bytes, 'B')
                else:
                    return bytes_to_array(ints_bytes, np.uint8)


    async def get_rng_int16s(self, n_ints, int_delta, output_type='array'):
        # int_delta = int_max - int_min
        if n_ints == 0:
            self.lg.error('{} RNG Ints: Provide n_ints > 0'.format(self.dev_name))
            return None
        if n_ints >= 2**16:
            self.lg.error('{} RNG Ints: Provide n_ints as a 16-bit integer'.format(self.dev_name))
            return None
        if int_delta >= 2**16:
            self.lg.error('{} RNG Ints: Provide int_delta as a 16-bit integer'.format(self.dev_name))
            return None
        if int_delta == 0:
            self.lg.error('{} RNG Ints: Provide int_delta > 0'.format(self.dev_name))
            return None

        comm = 'RNG_INT16S'
        if self.snd_rava_msg(comm, [n_ints, int_delta], 'HH'):
            ints_bytes = await self.get_queue_data(comm)
            if ints_bytes is None:
                return None
            else:
                if output_type == 'list':
                    return bytes_to_list(ints_bytes, 'H')
                else:
                    return bytes_to_array(ints_bytes, np.uint16)


    async def get_rng_floats(self, n_floats, output_type='array'):
        if n_floats == 0:
            self.lg.error('{} RNG Floats: Provide n_floats > 0'.format(self.dev_name))
            return None
        if n_floats >= 2**16:
            self.lg.error('{} RNG Floats: Provide n_floats as a 16-bit integer'.format(self.dev_name))
            return None

        comm = 'RNG_FLOATS'
        if self.snd_rava_msg(comm, [n_floats], 'H'):
            ints_bytes = await self.get_queue_data(comm)
            if ints_bytes is None:
                return None
            else:
                if output_type == 'list':
                    return bytes_to_list(ints_bytes, 'f')
                else:
                    return bytes_to_array(ints_bytes, np.float32)


    async def get_rng_byte_stream_data(self, output_type='array'):
        if not self.rng_streaming:
            self.lg.warning('{} RNG Stream: Streaming is disabled'.format(self.dev_name))
            return None, None

        comm = 'RNG_STREAM_BYTES'
        rng_bytes_a, rng_bytes_b = await self.get_queue_data(comm)

        if (rng_bytes_a is None) or (rng_bytes_b is None):
            return None, None

        else:
            if output_type == 'list':
                rng_a = bytes_to_list(rng_bytes_a, 'B')
                rng_b = bytes_to_list(rng_bytes_b, 'B')
                return rng_a, rng_b

            elif output_type == 'array':
                    rng_a = bytes_to_array(rng_bytes_a, np.uint8)
                    rng_b = bytes_to_array(rng_bytes_b, np.uint8)
                    return rng_a, rng_b

            else:
                return rng_bytes_a, rng_bytes_b


    async def get_rng_byte_stream_status(self):
        comm = 'RNG_STREAM_STATUS'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)


    ## HEALTH

    async def get_health_startup_results(self):
        comm = 'HEALTH_STARTUP_RESULTS'
        if self.snd_rava_msg(comm):
            success, pc_avg_vars, pc_avg_diff_vars, bias_bit_vars, bias_byte_vars = await self.get_queue_data(comm)
            data_vars = [pc_avg_vars, pc_avg_diff_vars, bias_bit_vars, bias_byte_vars]
            data_names = ['pulse_count', 'pulse_count_diff', 'bit_bias', 'byte_bias']
            return success, dict(zip(data_names, data_vars))


    async def get_health_continuous_errors(self):
        comm = 'HEALTH_CONTINUOUS_ERRORS'
        if self.snd_rava_msg(comm):
            data_vars = await self.get_queue_data(comm)
            n_errors = sum(data_vars)
            data_names = ['repetitive_count_a', 'repetitive_count_b',
                          'adaptative_proportion_a', 'adaptative_proportion_b']
            return n_errors, dict(zip(data_names, data_vars))


    ## PERIPHERALS

    async def get_periph_digi_state(self, periph_id=1):
        if periph_id == 0 or periph_id > 5:
            self.lg.error('{} Periph: Provide a periph_id between 1 and 5'.format(self.dev_name))
            return None

        comm = 'PERIPH_READ'
        if self.snd_rava_msg(comm, [periph_id], 'B'):
            digi_state, digi_mode = await self.get_queue_data(comm)
            return digi_state, D_PERIPH_MODES_INV[digi_mode]


    async def get_periph_d2_input_capture(self):
        comm = 'PERIPH_D2_TIMER3_INPUT_CAPTURE'
        return await self.get_queue_data(comm)


    async def get_periph_d5_adc_read(self, ref_5v=1, clk_prescaler=0, oversampling_n_bits=0, on=True):
        if clk_prescaler == 0 or clk_prescaler > 7:
            self.lg.error('{} Periph D5: Provide a clk_prescaler between 1 and 7'.format(self.dev_name))
            return None
        if oversampling_n_bits > 6:
            self.lg.error('{} Periph D5: Provide a oversampling_n_bits <= 6'.format(self.dev_name))
            return None

        comm = 'PERIPH_D5_ADC'
        if self.snd_rava_msg(comm, [on, ref_5v, clk_prescaler, oversampling_n_bits], 'BBBB'):
            if on:
                return await self.get_queue_data(comm)


    ## INTERFACES

    async def get_interface_ds18bs0(self):
        comm = 'INTERFACE_DS18B20'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)