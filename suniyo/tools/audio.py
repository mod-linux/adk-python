from hardware.speaker_driver import SpeakerDriver

class AudioController:
    def __init__(self):
        self.driver = SpeakerDriver()

    def speak(self, text: str):
        """Make the robot speak."""
        self.driver.speak(text)
        return f"Spoke: {text}"

    def bark(self, times: int = 1):
        """Make the robot bark."""
        for i in range(times):
            self.driver.speak("Woof!")
        return f"Barked {times} times."
