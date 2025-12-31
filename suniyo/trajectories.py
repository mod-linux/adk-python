import os
import math
import numpy as np
from google.adk.agents import Agent


# ====================================================
# CONFIG
# ====================================================

os.environ["GOOGLE_API_KEY"] = "AIzaSyDkauS7ezDGu3cKbGfZKDu4kXfBcpwmQIc"
MODEL = "gemini-2.0-flash"

# Leg dimensions
THIGH = 8.0
SHIN = 8.0

# Limits
LIMITS = {
    "hip":   (-45, 45),
    "knee":  (0, 110),
    "ankle": (-60, 10),
}


# ====================================================
# IK SOLVER — TOOL
# ====================================================

def ik_tool(target: dict) -> dict:
    """
    Input: {"x": <float>, "y": <float>}
    Output: {"hip": deg, "knee": deg, "ankle": deg}
    """

    x = target["x"]
    y = target["y"]

    L1 = THIGH
    L2 = SHIN

    dist = math.sqrt(x*x + y*y)

    if dist > (L1 + L2):
        raise ValueError("Unreachable target")

    # knee
    knee_angle = math.acos((L1*L1 + L2*L2 - dist*dist) / (2 * L1 * L2))
    knee = math.degrees(knee_angle)

    # hip
    hip_angle = math.atan2(y, x) - math.atan2(L2 * math.sin(knee_angle),
                                              L1 + L2 * math.cos(knee_angle))
    hip = math.degrees(hip_angle)

    # ankle keeps foot horizontal
    ankle = -(hip + knee)

    # clamp
    hip = np.clip(hip, LIMITS["hip"][0], LIMITS["hip"][1])
    knee = np.clip(knee, LIMITS["knee"][0], LIMITS["knee"][1])
    ankle = np.clip(ankle, LIMITS["ankle"][0], LIMITS["ankle"][1])

    return {
        "hip": float(round(hip, 2)),
        "knee": float(round(knee, 2)),
        "ankle": float(round(ankle, 2)),
    }


# ====================================================
# AGENT
# ====================================================

robot_agent = Agent(
    name="quadruped_ik_agent",
    model=MODEL,
    description=(
        "You are a robotics expert specializing in quadruped gait generation. "
        "You **must** generate foot positions for all 4 legs based purely on physics, "
        "biomechanics, gait theory, and kinematics. No hardcoded values. "
        "For each leg, create realistic 2D foot placement: {x,y}. "
        "Then call ik_tool for each foot to convert it into joint angles."
    ),
    instruction=(
        "User will give high-level commands like 'walk forward', 'walk backward', "
        "'turn left', 'turn right', 'stand'.\n"
        "\n"
        "You must:\n"
        "1. Analyze the command.\n"
        "2. Generate foot trajectories (x,y) for all 4 legs based on motion.\n"
        "   - You must compute stride length.\n"
        "   - You must compute lift height.\n"
        "   - You must maintain stability.\n"
        "   - Do NOT use any fixed values.\n"
        "   - Base values only on physical reasoning.\n"
        "\n"
        "3. Call ik_tool separately for each leg:\n"
        "   - front_left\n"
        "   - front_right\n"
        "   - rear_left\n"
        "   - rear_right\n"
        "\n"
        "4. Return a JSON with joint angles for all 4 legs.\n"
    ),
    tools=[ik_tool],
)