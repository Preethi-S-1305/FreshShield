import serial
import time

ports = ["COM3", "COM4", "COM10", "COM11"]

print("===================================")
print("   FRESHSHIELD HC-05 PORT TEST")
print("===================================")

for port in ports:

    print("\nTesting", port, "...")

    try:
        ser = serial.Serial(
            port,
            9600,
            timeout=2
        )

        print("Port opened successfully.")

        start = time.time()
        received = False

        while time.time() - start < 5:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if line:
                print("RECEIVED:", line)
                received = True

        ser.close()

        if received:
            print(">>> HC-05 DATA FOUND ON", port)
        else:
            print("No data received.")

    except Exception as e:
        print("Cannot use", port)
        print("Reason:", e)

print("\n===================================")
print("TEST COMPLETE")
print("===================================")