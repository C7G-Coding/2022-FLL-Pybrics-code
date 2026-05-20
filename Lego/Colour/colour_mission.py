#!/usr/bin/env pybricks-micropython
"""
Line following with distance-based waypoints and turns.
The robot follows the line using the color sensor, but can execute
specific turns at pre-programmed distances.
Stops automatically when reaching the end of a line.
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
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(threshold))
    
    print("Calibration Complete. Threshold: " + str(threshold))
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
            if steering > 75:
                steering = 75
            if steering < -75:
                steering = -75
            
            self.robot.drive(self.drive_speed, steering)
            
            # Small delay for stability
            wait(10)
    
    def follow_line_until_end(self, max_distance=1000):
        """
        Follow line until the end is detected (sensor sees white for extended period)
        
        Args:
            max_distance: Maximum distance to travel as safety limit (mm)
        """
        start_distance = self.robot.distance()
        white_detected_count = 0
        WHITE_THRESHOLD = 5  # Number of consecutive white readings to confirm end
        
        while True:
            # Safety check - don't go too far
            traveled = abs(self.robot.distance() - start_distance)
            if traveled > max_distance:
                self.robot.stop()
                print("Max distance reached - stopping")
                ev3.screen.draw_text(0, 80, "Max distance reached")
                break
            
            reflection = line_sensor.reflection()
            
            # Check if we've reached the end of the line
            if reflection > self.threshold:  # Seeing white (no line)
                white_detected_count += 1
                if white_detected_count >= WHITE_THRESHOLD:
                    self.robot.stop()
                    print("End of line detected!")
                    ev3.screen.draw_text(0, 80, "End of line detected!")
                    break
            else:
                white_detected_count = 0  # Reset if we see line again
            
            # Normal line following
            error = reflection - self.threshold
            steering = error * self.kp
            
            if steering > 75:
                steering = 75
            if steering < -75:
                steering = -75
            
            self.robot.drive(self.drive_speed, steering)
            
            # Show debug info
            ev3.screen.draw_text(0, 60, "Traveled: " + str(int(traveled)) + "mm")
            ev3.screen.draw_text(0, 70, "White cnt: " + str(white_detected_count))
            
            wait(10)
    
    def follow_line_hybrid(self, distance_mm, stop_at_line_end=True):
        """
        Follow line for specified distance OR until line ends, whichever comes first
        
        Args:
            distance_mm: Distance to travel in mm
            stop_at_line_end: Whether to stop when end of line is detected
        """
        start_distance = self.robot.distance()
        white_detected_count = 0
        WHITE_THRESHOLD = 5
        
        while True:
            traveled = abs(self.robot.distance() - start_distance)
            reflection = line_sensor.reflection()
            
            # Check if we've reached the distance goal
            distance_reached = (traveled >= distance_mm)
            
            # Check if we've reached the line end
            line_end_detected = False
            if stop_at_line_end:
                if reflection > self.threshold:
                    white_detected_count += 1
                    if white_detected_count >= WHITE_THRESHOLD:
                        line_end_detected = True
                else:
                    white_detected_count = 0
            
            # Stop if either condition is met
            if distance_reached or line_end_detected:
                self.robot.stop()
                
                if distance_reached:
                    print("Stopped: Distance reached (" + str(int(traveled)) + "mm)")
                    ev3.screen.draw_text(0, 70, "Distance target reached")
                if line_end_detected:
                    print("Stopped: End of line detected")
                    ev3.screen.draw_text(0, 70, "Line end detected")
                
                wait(1000)
                break
            
            # Normal line following
            error = reflection - self.threshold
            steering = error * self.kp
            
            if steering > 75:
                steering = 75
            if steering < -75:
                steering = -75
            
            self.robot.drive(self.drive_speed, steering)
            
            # Show debug info
            ev3.screen.draw_text(0, 50, "Traveled: " + str(int(traveled)) + "/" + str(distance_mm) + "mm")
            ev3.screen.draw_text(0, 60, "White cnt: " + str(white_detected_count))
            
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
        angles = [30, -60, 30]
        for angle in angles:
            self.robot.turn(angle, 50)
            wait(200)
            
            if line_sensor.reflection() < self.threshold:
                ev3.screen.draw_text(0, 80, "Line found!")
                ev3.speaker.beep(800, 100)
                return True
        
        return False
    
    def measure_line_length(self):
        """
        Measure the length of the current line by driving to the end.
        Returns the length in mm.
        """
        self.robot.reset()
        start_distance = self.robot.distance()
        
        print("Measuring line length...")
        ev3.screen.clear()
        ev3.screen.draw_text(0, 20, "Measuring line...")
        ev3.screen.draw_text(0, 40, "Drive to end of line")
        wait(2000)
        
        white_count = 0
        while white_count < 5:
            reflection = line_sensor.reflection()
            
            if reflection > self.threshold:
                white_count += 1
            else:
                white_count = 0
            
            error = reflection - self.threshold
            steering = error * self.kp
            
            if steering > 75:
                steering = 75
            if steering < -75:
                steering = -75
            
            self.robot.drive(80, steering)
            wait(10)
        
        self.robot.stop()
        end_distance = self.robot.distance()
        length = abs(end_distance - start_distance)
        
        print("Line length: " + str(int(length)) + "mm")
        ev3.screen.clear()
        ev3.screen.draw_text(0, 20, "Line length measured!")
        ev3.screen.draw_text(0, 40, "Length: " + str(int(length)) + "mm")
        wait(3000)
        
        return length

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
    
    # OPTIONAL: Measure your line length first (uncomment to use)
    # line_length = follower.measure_line_length()
    # wait(1000)
    
    print("Starting course execution...")
    
    # ===== DEFINE YOUR COURSE HERE =====
    # The robot will follow the line and automatically stop at the end
    # Adjust distances based on your track
    
    # SEGMENT 1: Follow line until the end (automatically detects end)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Segment 1: Following line")
    ev3.screen.draw_text(0, 40, "Will stop at line end")
    wait(1000)
    
    # This will follow the line and stop automatically when reaching the end
    follower.follow_line_until_end(max_distance=1000)
    ev3.screen.draw_text(0, 70, "Segment 1 complete!")
    ev3.speaker.beep(600, 100)
    wait(1000)
    
    # SEGMENT 2: Turn left 90 degrees
    follower.turn_degrees(-90)  # Negative = left, Positive = right
    
    # SEGMENT 3: Follow next line until the end
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Segment 2: Following next line")
    follower.follow_line_until_end(max_distance=1000)
    ev3.screen.draw_text(0, 70, "Segment 2 complete!")
    ev3.speaker.beep(700, 100)
    wait(1000)
    
    # SEGMENT 4: Turn right 90 degrees
    follower.turn_degrees(90)
    
    # SEGMENT 5: Follow line with hybrid approach (distance OR line end)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Segment 3: Following line")
    ev3.screen.draw_text(0, 40, "Max distance: 500mm")
    # This will stop after 500mm OR when line ends
    follower.follow_line_hybrid(500, stop_at_line_end=True)
    ev3.screen.draw_text(0, 70, "Segment 3 complete!")
    ev3.speaker.beep(800, 100)
    wait(1000)
    
    # SEGMENT 6: Final turn
    follower.turn_degrees(45)
    
    # SEGMENT 7: Last segment
    follower.follow_line_until_end(max_distance=500)
    
    # Finish
    follower.robot.stop()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Course Complete!")
    ev3.speaker.beep(1000, 500)
    ev3.speaker.beep(1200, 500)
    
    # Display total distance traveled
    total_distance = abs(follower.robot.distance())
    ev3.screen.draw_text(0, 60, "Total: " + str(int(total_distance)) + "mm")
    
    # Keep displaying completion message
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
    wait(2000)
    
    # Use while loop instead of for loop for compatibility
    i = 0
    while i < len(waypoints):
        distance, turn, description = waypoints[i]
        
        # Display current waypoint
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Waypoint " + str(i+1) + "/" + str(len(waypoints)))
        ev3.screen.draw_text(0, 20, description)
        ev3.screen.draw_text(0, 40, "Distance: " + str(distance) + "mm")
        
        # Follow line to this waypoint (stops at line end if reached early)
        follower.follow_line_hybrid(distance, stop_at_line_end=True)
        
        # Execute turn (if any)
        if turn != 0:
            ev3.screen.draw_text(0, 60, "Turning " + str(turn) + " degrees...")
            follower.turn_degrees(turn)
        
        wait(1000)
        i += 1
    
    # Finished all waypoints
    follower.robot.stop()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "All waypoints complete!")
    ev3.speaker.beep(1000, 500)
    
    while True:
        wait(1000)

# =============================================================================
# SIMPLE MODE: Just follow until line ends
# =============================================================================

def simple_line_follow():
    """
    Very simple mode: Just calibrate and follow the line until it ends.
    Perfect for testing or simple courses.
    """
    black, white, threshold = calibrate()
    follower = LineFollowerWithWaypoints(black, white, threshold)
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Following line...")
    ev3.screen.draw_text(0, 60, "Will stop at end")
    wait(2000)
    
    # Follow until the line ends
    follower.follow_line_until_end(max_distance=2000)
    
    ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "Line finished!")
    ev3.speaker.beep(1000, 500)
    
    while True:
        wait(1000)

# =============================================================================
# RUN THE PROGRAM
# =============================================================================

if __name__ == "__main__":
    # Choose which mode to run:
    
    # Mode 1: Simple distance-based navigation with automatic line end detection
    main()
    
    # Mode 2: Advanced waypoint navigation (uncomment to use)
    # dynamic_waypoint_navigation()
    
    # Mode 3: Super simple - just follow one line until it ends (uncomment to use)
    # simple_line_follow()