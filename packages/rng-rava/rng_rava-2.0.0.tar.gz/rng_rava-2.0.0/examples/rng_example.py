'''
RAVA RNG usage example.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import rng_rava as rava

# Find the serial number of the attached RAVA devices
rava_sns = rava.find_rava_sns()

# Create a RNG instance and connect to the first device
rng = rava.RAVA_RNG()
rng.connect(serial_number=rava_sns[0])

'''
The default PWM BOOST and RNG configuration parameters are stored in the EEPROM 
memory and can be accessed with rng.get_eeprom_pwm_boost() and 
rng.get_eeprom_rng(). If desired, users can modify the default values using the 
respective snd_ functions. Additionally, it is possible to make non-permanent 
configuration changes using the following commands:
'''

# Configure PWM
rng.snd_pwm_boost_setup(freq_id=rava.D_PWM_BOOST_FREQ['50_KHZ'], duty=20)

# Configure RNG
rng.snd_rng_setup(sampling_interval_us=10)

'''
Next, the generation of various random data types is demonstrated.
'''

# Measure 100 pulse counts
pc_a, pc_b = rng.get_rng_pulse_counts(n_counts=100)

# Generate a random bit XORing both channels
bit = rng.get_rng_bits(bit_source_id=rava.D_RNG_BIT_SRC['AB_XOR'])

# Generate 100 random bytes en each channel without post-processing
bytes_a, bytes_b = rng.get_rng_bytes(n_bytes=100, postproc_id=rava.D_RNG_POSTPROC['NONE'])

# Generate 100 8-bit integers between 0 and 99
ints8 = rng.get_rng_int8s(n_ints=100, int_delta=99)

# Generate 100 16-bit integers between 0 and 9999
ints16 = rng.get_rng_int16s(n_ints=100, int_delta=9999)

# Generate 100 32-bit floats ranging between 0 and 1
floats = rng.get_rng_floats(n_floats=100)

# Close RAVA device
rng.close()