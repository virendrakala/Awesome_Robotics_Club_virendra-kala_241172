import math

# Segment lengths (in same units)
L1 = 5.0   # Coxa
L2 = 10.0  # Femur
L3 = 15.0  # Tibia
b = 0.0    # Base offset from ground (set to 0 unless known)

def inverse_kinematics(x, y, z):
    # Coxa angle (rotation in horizontal plane)
    q1 = math.atan2(y, x)

    # Distance from base to foot in horizontal plane
    r = math.sqrt(x**2 + y**2)
    
    # Adjusted vertical distance from coxa joint to foot
    dz = z - L1 - b

    # Law of cosines to find tibia angle
    D = (r**2 + dz**2 - L2**2 - L3**2) / (2 * L2 * L3)

    # Check for unreachable target (invalid cos value)
    if D < -1 or D > 1:
        return None, None, None

    # Tibia angle (gamma)
    q3 = math.acos(D)

    # Femur angle (beta)
    s3 = math.sin(q3)
    c3 = math.cos(q3)

    q2 = math.atan2(dz, r) - math.atan2(s3 * L3, L2 + c3 * L3)

    # Convert all to degrees
    alpha = math.degrees(q1)
    beta = math.degrees(q2)
    gamma = math.degrees(q3)

    return alpha, beta, gamma


# TEST FUNCTION


def test_inverse_kinematics():
    print("\n Running 5 Inverse Kinematics Tests\n")

    # List of test cases
    test_cases = [
        {"desc": "Typical reachable point", "x": 10, "y": 5, "z": -10},
        {"desc": "Close to base", "x": 1, "y": 1, "z": -2},
        {"desc": "Near max reach", "x": 25, "y": 0, "z": -5},
        {"desc": "Unreachable point", "x": 35, "y": 10, "z": 0},
        {"desc": "Large negative z", "x": 5, "y": 5, "z": -30}
    ]

    for i, test in enumerate(test_cases, start=1):
        x, y, z = test["x"], test["y"], test["z"]
        print(f" Test {i}: {test['desc']} ")
        print(f"x: {x}, y: {y}, z: {z}")

        angles = inverse_kinematics(x, y, z)

        if None in angles:
            print("Target is unreachable.\n")
        else:
            alpha, beta, gamma = angles
            print("Target is reachable.")
            print(f"  Coxa (α):  {alpha:.2f}°")
            print(f"  Femur (β): {beta:.2f}°")
            print(f"  Tibia (γ): {gamma:.2f}°\n")

# MANUAL INPUT 

if __name__ == "__main__":
    
    x = float(input("Enter x-coordinate of the foot: "))
    y = float(input("Enter y-coordinate of the foot: "))
    z = float(input("Enter z-coordinate of the foot: "))

    angles = inverse_kinematics(x, y, z)

    if None in angles:
        print("Target is unreachable.")
    else:
        alpha, beta, gamma = angles
        print("\nRequired Joint Angles:")
        print(f"Coxa (α):  {alpha:.2f}°")
        print(f"Femur (β): {beta:.2f}°")
        print(f"Tibia (γ): {gamma:.2f}°")
    

    # Run test cases
    test_inverse_kinematics()