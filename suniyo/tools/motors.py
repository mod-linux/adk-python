# tools/motors.py

from hardware.motor_driver import MotorDriver

class MotorController:
    def __init__(self):
        self.driver = MotorDriver()

    def move_servo(self, servo_id: int, angle: float):
        """Move a servo to a specific angle."""
        self.driver.set_servo_angle(servo_id, angle)
        return f"Moved servo {servo_id} to {angle} degrees."

    def walk_forward(self, steps: int):
        """Walk forward a number of steps."""
        for _ in range(steps):
            print("[MotorController] Walking step")
        return f"Walked {steps} steps."
