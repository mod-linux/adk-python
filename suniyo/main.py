import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import create_robot_agent
#from trajectories import robot_agent

# ====================================================
# ADK SESSION SETUP
# ====================================================

session_service = InMemorySessionService()
APP = "quadruped_app"
USER = "user123"
SESSION = "session1"

robot_agent = create_robot_agent()

asyncio.get_event_loop().run_until_complete(
    session_service.create_session(app_name=APP, user_id=USER, session_id=SESSION)
)

runner = Runner(agent=robot_agent, app_name=APP, session_service=session_service)


# ====================================================
# CLI
# ====================================================

async def ask_robot(cmd: str):
    content = types.Content(role="user", parts=[types.Part(text=cmd)])
    final = ""

    async for event in runner.run_async(user_id=USER, session_id=SESSION, new_message=content):
        if event.is_final_response():
            final = event.content.parts[0].text
            break

    print("\n==== ROBOT RESPONSE ====")
    print(final)
    print("========================\n")


async def main():
    print("Quadruped Control")
    print("Type: walk forward | walk backward | turn left | turn right | stand | exit\n")

    while True:
        q = input("> ").strip()
        if q == "exit":
            break
        await ask_robot(q)

if __name__ == "__main__":
    asyncio.run(main())
