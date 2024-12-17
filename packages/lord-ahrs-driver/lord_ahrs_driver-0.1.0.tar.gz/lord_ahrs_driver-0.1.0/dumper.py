import serial
# Use this script to dump the raw data from the IMU to a file. This is useful for debugging and for offline analysis.


with serial.Serial('/dev/tty.usbserial-ALBGb121474', 115200) as ser, open('dump3.txt', 'wb') as f:
    n = 0
    while True:
        x = ser.read()          # read one byte
        f.write(x)              # write to the file
        if n % 10000 == 0:
            print(n)
            f.flush()           # flush the file buffer
        n += 1