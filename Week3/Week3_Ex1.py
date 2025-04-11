from machine import Pin, PWM
import time
import array

# Importing the custom libraries (assuming you uploaded them as modules)
from fifo import Fifo
from led import Led

class RotaryEncoderLedControl:
    
    def __init__(self, encoder_clk_pin, encoder_dt_pin, encoder_button_pin, led_pin):
        # Initialize components
        self.encoder_clk = Pin(encoder_clk_pin, Pin.IN, Pin.PULL_UP)
        self.encoder_dt = Pin(encoder_dt_pin, Pin.IN, Pin.PULL_UP)
        self.encoder_button = Pin(encoder_button_pin, Pin.IN, Pin.PULL_UP)
        self.led = Led(led_pin)
        self.fifo = Fifo(10, 'h')  # FIFO buffer for encoder events
        
        self.led_on = False
        self.brightness = 0  # Initial brightness
        self.brightness_step=2

        self.last_button_state = 1
        self.button_debounce_time = 0.2  # 200ms debounce time

        # Set up encoder interrupts
        self.encoder_clk.irq(handler=self.encoder_interrupt_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING )
        
    def encoder_interrupt_handler(self, pin):
        if self.encoder_clk.value() != self.encoder_dt.value():
            try:
                self.fifo.put(1)  # Clockwise turn event
            except RuntimeError:
                pass
        else:
            try:
                self.fifo.put(-1)  # Counter-clockwise turn event
            except RuntimeError:
                pass

    def button_polling(self):
        current_button_state = self.encoder_button.value()

        if current_button_state == 0 and self.last_button_state == 1:
            time.sleep(self.button_debounce_time)  # Debounce delay
            if self.encoder_button.value() == 0:
                self.led_on = not self.led_on  # Toggle LED state
                self.led.value(1 if self.led_on else 0)  # Turn LED on/off based on led_on state
                print(f"LED {'ON' if self.led_on else 'OFF'}")

        self.last_button_state = current_button_state

    def process_encoder(self):
        if self.led_on:
            try:
                turn = self.fifo.get()
                self.brightness += turn * self.brightness_step  # Adjust brightness step
                self.brightness = max(0, min(100, self.brightness))  # Keep brightness in range [0, 100]
                self.led.brightness(self.brightness)
                print(f"Brightness: {self.brightness}%")
            except RuntimeError:
                pass

    def run(self):
        while True:
            # Poll the button for debouncing
            self.button_polling()

            # Process encoder turns to adjust brightness if the LED is on
            self.process_encoder()



# Instantiate the RotaryEncoderLedControl class and start the program
control_system = RotaryEncoderLedControl(encoder_clk_pin=10, encoder_dt_pin=11, encoder_button_pin=12, led_pin=22)
control_system.run()
