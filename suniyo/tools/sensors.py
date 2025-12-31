from hardware.sensor_driver import SensorDriver

class SensorController:
    def __init__(self):
        self.driver = SensorDriver()

    def read_imu(self):
        """Read IMU orientation."""
        return self.driver.get_imu()

    def read_distance(self):
        """Read distance sensor."""
        return self.driver.get_distance()
