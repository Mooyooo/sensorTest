import serial
import time
import pynmea2

# --- Configuration ---
# You may need to change the port and baud rate to match your specific GNSS device.
SERIAL_PORT = '/dev/tty.usbmodem2201'
BAUD_RATE = 9600

def read_and_print_data():
    """
    Connects to the specified serial port and prints incoming data with
    additional debugging information.
    """
    print(f"Attempting to connect to port: {SERIAL_PORT} at baud rate: {BAUD_RATE}")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Connection successful! Reading data...")
        print("---")
        print("NOTE: Please ensure your GNSS device has a clear view of the sky.")
        print("It may take a few minutes to acquire a satellite fix.")
        print("---")

        while True:
            line = ser.readline()
            if line:
                try:
                    decoded_line = line.decode('utf-8').strip()
                    print(f"RAW DATA: {decoded_line}")
                    
                    # Try to parse the NMEA sentence
                    if decoded_line.startswith(('$GNGGA', '$GPGGA')):
                        msg = pynmea2.parse(decoded_line)
                        print(f"  Parsed Sentence: {msg.sentence_type}")
                        print(f"  Timestamp: {msg.timestamp}")
                        print(f"  Latitude: {msg.latitude:.6f}")
                        print(f"  Longitude: {msg.longitude:.6f}")
                        print(f"  Fix Quality: {msg.gps_qual}")
                        print(f"  Satellites in Use: {msg.num_sats}")
                        
                        if msg.gps_qual > 0:
                            print("  Status: VALID FIX ACQUIRED!")
                        else:
                            print("  Status: NO FIX. Waiting for satellites...")

                except pynmea2.ParseError as e:
                    print(f"  NMEA parsing error: {e}")
                except UnicodeDecodeError:
                    print("Could not decode line, skipping.")
            
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error: Could not open port {SERIAL_PORT}.")
        print(f"Please check if the device is connected and the port name is correct.")
        print(f"The error message was: {e}")
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    read_and_print_data()
