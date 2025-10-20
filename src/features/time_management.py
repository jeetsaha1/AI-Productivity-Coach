# class TimeManagement:
#     def start_timer(self, data):
#         print("Timer started with data:", data)

import time

def set_timer(seconds):
    print(f"⏳ Timer started for {seconds} seconds...")
    time.sleep(1)  # shortened for demo
    print("⏰ Time’s up!")

def demo():
    print("\n--- Time Management ---")
    set_timer(2)
