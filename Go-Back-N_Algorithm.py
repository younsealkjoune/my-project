import socket
import time
import threading
import random

class Sender:
    def __init__(self, window_size, timeout):
        self.window_size = window_size
        self.timeout = timeout
        self.base = 0
        self.next_seq_num = 0
        self.timer = None
        self.lock = threading.Lock()
        self.acknowledged = []

    def send_packet(self, packet):
        print(f"Sending packet {packet}")
        self.acknowledged.append(False)
        if self.base == self.next_seq_num:
            self.start_timer()
        self.next_seq_num += 1

    def start_timer(self):
        self.timer = threading.Timer(self.timeout, self.timeout_event)
        self.timer.start()

    def timeout_event(self):
        print("Timeout occurred. Resending packets...")
        self.lock.acquire()
        for i in range(self.base, self.next_seq_num):
            if not self.acknowledged[i]:
                print(f"Resending packet {i}")
        self.start_timer()
        self.lock.release()

    def receive_ack(self, ack):
        self.lock.acquire()
        if ack >= self.base:
            print(f"Acknowledgement received for packet {ack}")
            self.acknowledged[ack] = True
            self.base = ack + 1
            if self.base == self.next_seq_num:
                self.timer.cancel()
            else:
                self.start_timer()
        self.lock.release()

class Network:
    def __init__(self, sender, receiver, packet_loss_probability):
        self.sender = sender
        self.receiver = receiver
        self.packet_loss_probability = packet_loss_probability

    def send(self, packet):
        if random.random() > self.packet_loss_probability:
            self.receiver.receive(packet)
        else:
            print(f"Packet {packet} lost in transit")

class Receiver:
    def __init__(self):
        self.expected_seq_num = 0

    def receive(self, packet):
        print(f"Packet {packet} received")
        if packet == self.expected_seq_num:
            self.expected_seq_num += 1
            sender.receive_ack(packet)

# Initialize components
window_size = 4
timeout = 5
packet_loss_probability = 0.2

sender = Sender(window_size, timeout)
receiver = Receiver()
network = Network(sender, receiver, packet_loss_probability)

# Simulate sending packets
for packet in range(10):
    if sender.next_seq_num < sender.base + sender.window_size:
        network.send(packet)
        time.sleep(1)
    else:
        time.sleep(1)

print("Transmission finished.")
