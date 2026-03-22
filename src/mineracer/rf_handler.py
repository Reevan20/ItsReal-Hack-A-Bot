from pyrf24 import RF24
import time

class RFHandler:
    def __init__(self):
        # CE pin, CSN pin
        self.radio = RF24(22, 0)

        if not self.radio.begin():
            raise RuntimeError("NRF24 not responding")

        print("NRF24 initialized")

        # Config
        self.radio.set_pa_level(RF24.PA_LOW)
        self.radio.set_channel(76)
        self.radio.set_payload_size(32)

        # Addresses (must match Pico)
        self.tx_address = b"1Node"
        self.rx_address = b"2Node"

        self.radio.open_tx_pipe(self.tx_address)
        self.radio.open_rx_pipe(1, self.rx_address)

        self.radio.stop_listening()

    def send(self, msg: str):
        data = msg.encode("utf-8")
        data = data.ljust(32, b'\0')

        success = self.radio.write(data)

        if success:
            print(f"✅ Sent: {msg}")
        else:
            print("❌ Send failed")

    def receive(self):
        self.radio.start_listening()

        if self.radio.available():
            received = self.radio.read()
            decoded = received.decode("utf-8").strip('\x00')

            print(f"📩 Received: {decoded}")

            self.radio.stop_listening()
            return decoded

        self.radio.stop_listening()
        return None
