from google.adk.agents import Agent
from tools.motors import MotorController
from tools.sensors import SensorController
from tools.audio import AudioController

def create_robot_agent():
    return Agent(
        name="robot_dog_agent",
        instructions=(
            "You control the robotic dog. "
            "Use the available tools to move, read sensors, and speak. "
            "Always act safely and avoid harmful movements."
        ),
        tools=[
            MotorController(),
            SensorController(),
            AudioController(),
        ],
    )
