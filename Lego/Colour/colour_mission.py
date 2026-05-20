#!/usr/bin/env pybricks-micropython
"""
Line following with distance-based waypoints and turns.
The robot follows the line using the color sensor, but can execute
specific turns at pre-programmed distances.
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
line_sensor = ColorSensor(Port.S3)

# Wheel diameter: 56mm, axle track: 121mm
robot = DriveBase(left_motor, right_motor, 56, 121)

# =============================================================================
# CALIBRATION
# =============================================================================

def calibrate():
    """Calibrate black and white values"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK")
    ev3.screen.draw_text(0, 50, "Press any btn")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    black_value = line_sensor.reflection()
    ev3.speaker.beep(500, 200)
    
    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on WHITE")
    ev3.screen.draw_text(0, 50, "Press any btn")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    white_value = line_sensor.reflection()
    ev3.speaker.beep(1000, 200)
    
    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    
    threshold = (black_value + white_value) / 2
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, f"Blk: {black_value}")
    ev3.screen.draw_text(0, 30, f"Wht: {white_value}")
    ev3.screen.draw_text(0, 60, f"Thr: {threshold:.1f}")
    
    print(f"Calibration Complete. Threshold: {threshold}")
    wait(2000)
    
    return black_value, white_value, threshold

# =============================================================================
# LINE FOLLOWING WITH DISTANCE TRIGGERS
# =============================================================================

class LineFollowerWithWaypoints:
    def __init__(self, black, white, threshold):
        self.black = black
        self.white = white
        self.threshold = threshold
        self.drive_speed = 100
        self.kp = 1.2  # Proportional gain
        self.robot = robot
        
        # Reset the distance counter
        self.robot.reset()
        
    def follow_line(self, distance_mm=None, stop_at_end=True):
        """
        Follow the line for a specified distance.
        
        Args:
            distance_mm: Distance to travel in mm (None = infinite)
            stop_at_end: Whether to stop when distance is reached
        """
        start_distance = self.robot.distance()
        
        while True:
            # Check if we've traveled the required distance
            if distance_mm is not None:
                traveled = abs(self.robot.distance() - start_distance)
                if traveled >= distance_mm:
                    if stop_at_end:
                        self.robot.stop()
                    break
            
            # Line following logic
            reflection = line_sensor.reflection()
            error = reflection - self.threshold
            steering = error * self.kp
            
            # Limit steering to prevent spinning
            steering = max(-75, min(75, steering))
            
            self.robot.drive(self.drive_speed, steering)
            
            # Small delay for stability
            wait(10)
    
    def turn_degrees(self, angle, speed=80):
        """
        Turn a specific number of degrees.
        Positive = right, Negative = left
        """
        self.robot.stop()
        wait(100)
        self.robot.turn(angle, speed)
        wait(100)
        self.robot.reset()  # Reset distance after turn
    
    def turn_to_heading(self, heading, speed=80):
        """
        Turn to an absolute heading (0-360 degrees).
        """
        self.robot.stop()
        wait(100)
        self.robot.turn(heading - self.robot.angle(), speed)
        wait(100)
        self.robot.reset()
    
    def straight(self, distance_mm, speed=100):
        """
        Drive straight for a specific distance (ignores line).
        Useful for crossing gaps.
        """
        self.robot.stop()
        self.robot.reset()
        self.robot.straight(distance_mm, speed)
        wait(100)
        self.robot.reset()
    
    def search_for_line(self):
        """
        If line is lost, search for it by wiggling.
        """
        ev3.screen.draw_text(0, 80, "Searching for line...")
        
        # Wiggle pattern to find line
        for angle in [30, -60, 30]:
            self.robot.turn(angle, 50)
            wait(200)
            
            if line_sensor.reflection() < self.threshold:
                ev3.screen.draw_text(0, 80, "Line found!")
                ev3.speaker.beep(800, 100)
                return True
        
        return False

# =============================================================================
# MAIN PROGRAM - CUSTOMIZABLE COURSE
# =============================================================================

def main():
    # Calibrate the sensor
    black, white, threshold = calibrate()
    
    # Create the line follower
    follower = LineFollowerWithWaypoints(black, white, threshold)
    
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Starting Course...")
    wait(2000)
    
    # ===== DEFINE YOUR COURSE HERE =====
    # The robot will follow the line for the specified distances,
    # then execute the turns exactly at those points.
    
    # Example Course 1: Square with 4 turns
    """
    follower.follow_line(300)      # Follow line for 300mm
    follower.turn_degrees(90)       # Turn right 90 degrees
    follower.follow_line(300)      # Follow line for 300mm
    follower.turn_degrees(90)       # Turn right 90 degrees
    follower.follow_line(300)      # Follow line for 300mm
    follower.turn_degrees(90)       # Turn right 90 degrees
    follower.follow_line(300)      # Follow line for 300mm
    follower.turn_degrees(90)       # Turn right 90 degrees (back to start)
    """
    
    # Example Course 2: Complex path with mixed line following and straights
    """
    follower.follow_line(500)       # Follow line for 500mm
    follower.turn_degrees(45)       # Turn right 45 degrees
    follower.follow_line(200)       # Follow line for 200mm
    follower.turn_degrees(-90)      # Turn left 90 degrees
    follower.straight(100)          # Drive straight for 100mm (cross gap)
    follower.follow_line(300)       # Follow line for 300mm
    follower.turn_degrees(135)      # Turn right 135 degrees
    follower.follow_line(400)       # Follow line for 400mm
    """
    
    # Example Course 3: With T-junction decision at specific point
    """
    follower.follow_line(400)       # Follow line to T-junction
    follower.turn_degrees(-90)      # Turn left at T-junction
    follower.follow_line(250)       # Follow new line
    follower.turn_degrees(90)       # Turn right
    follower.follow_line(300)       # Follow line to end
    """
    
    # ACTIVE COURSE - Modify this section for your track:
    print("Starting course execution...")
    
    # SEGMENT 1: Follow line for 400mm
    follower.follow_line(400)
    ev3.screen.draw_text(0, 70, "Waypoint 1 reached!")
    ev3.speaker.beep(600, 100)
    wait(500)
    
    # SEGMENT 2: Turn left 90 degrees
    follower.turn_degrees(-90)  # Negative = left, Positive = right
    
    # SEGMENT 3: Follow line for 300mm
    follower.follow_line(300)
    ev3.screen.draw_text(0, 70, "Waypoint 2 reached!")
    ev3.speaker.beep(700, 100)
    wait(500)
    
    # SEGMENT 4: Turn right 90 degrees
    follower.turn_degrees(90)
    
    # SEGMENT 5: Follow line for 500mm
    follower.follow_line(500)
    ev3.screen.draw_text(0, 70, "Waypoint 3 reached!")
    ev3.speaker.beep(800, 100)
    wait(500)
    
    # SEGMENT 6: Final turn and short follow
    follower.turn_degrees(45)
    follower.follow_line(200)
    
    # Finish
    follower.robot.stop()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Course Complete!")
    ev3.speaker.beep(1000, 500)
    ev3.speaker.beep(1200, 500)
    
    # Display total distance traveled
    total_distance = abs(follower.robot.distance())
    ev3.screen.draw_text(0, 70, f"Total: {total_distance:.0f}mm")
    
    while True:
        wait(1000)

# =============================================================================
# ADVANCED: Dynamic Waypoint Navigation
# =============================================================================

def dynamic_waypoint_navigation():
    """
    Advanced example: Follow line until reaching a specific sensor reading
    or distance, then execute a turn.
    """
    black, white, threshold = calibrate()
    follower = LineFollowerWithWaypoints(black, white, threshold)
    
    # Define waypoints as (distance_mm, turn_angle, description)
    waypoints = [
        (300, 90, "First corner - turn right"),
        (250, -90, "Second corner - turn left"),
        (400, 0, "Straight section - no turn"),
        (200, 45, "Merge - slight right"),
        (350, -135, "Exit - sharp left"),
    ]
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Starting waypoint navigation")
    
    for i, (distance, turn, description) in enumerate(waypoints):
        # Display current waypoint
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, f"Waypoint {i+1}/{len(waypoints)}")
        ev3.screen.draw_text(0, 20, description)
        ev3.screen.draw_text(0, 40, f"Distance: {distance}mm")
        
        # Follow line to this waypoint
        follower.follow_line(distance)
        
        # Execute turn (if any)
        if turn != 0:
            ev3.screen.draw_text(0, 60, f"Turning {turn} degrees...")
            follower.turn_degrees(turn)
        
        wait(1000)
    
    # Finished all waypoints
    follower.robot.stop()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "All waypoints complete!")
    ev3.speaker.beep(1000, 500)

# =============================================================================
# RUN THE PROGRAM
# =============================================================================

if __name__ == "__main__":
    # Choose which mode to run:
    
    # Mode 1: Simple distance-based navigation
    main()
    
    # Mode 2: Advanced waypoint navigation (uncomment to use)
    # dynamic_waypoint_navigation()