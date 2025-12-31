class MotorDriver:
    def __init__(self):
        print("Motors initialized")

    def set_servo_angle(self, servo_id: int, angle: float):
        print(f"[MotorDriver] Servo {servo_id} → {angle}°")
        # TODO: send PWM or Dynamixel command
