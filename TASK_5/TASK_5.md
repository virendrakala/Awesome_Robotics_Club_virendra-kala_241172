# TASK 5: Inverse Kinematics for a 3-DOF Hexapod Leg

##  Problem Statement
Design and implement a Python-based solution for computing inverse kinematics of a 3-DOF hexapod leg. The system should determine the joint angles required to position the foot at a specified 3D coordinate. The solution must include test cases for validation

## Leg Configuration

- **Coxa (L1)**: 5.0 units
- **Femur (L2)**: 10.0 units
- **Tibia (L3)**: 15.0 units
- **Base height offset (b)**: 0.0 (assumed at ground level)

The joints allow the leg to move in 3D space with 3 Degrees of Freedom (DOF). The three joint angles are:
- **α (alpha)** – Coxa rotation
- **β (beta)** – Femur rotation
- **γ (gamma)** – Tibia rotation 

## Kinematics Approach

### Step-by-step Process:
1. **Calculate α (Coxa Angle)**:
   - Using `atan2(y, x)` to get the yaw angle in the horizontal plane.

2. **Compute horizontal and vertical distances**:
   - `r` = √(x² + y²)
   - `dz` = z - L1 - b

3. **Use Law of Cosines to calculate γ (Tibia Angle)**:
   - `D = (r² + dz² - L2² - L3²) / (2 * L2 * L3)`
   - `γ = acos(D)`

4. **Calculate β (Femur Angle)**:
   - Using a two-part angle formula:
     - `atan2(dz, r)` and `atan2(sin(γ) * L3, L2 + cos(γ) * L3)`

5. **Convert all angles from radians to degrees**.

6. **Check for unreachable targets**:
   - If `D` lies outside [-1, 1], return `None` for all angles.

## Test Scenarios

| Test | Description                     | Input (x, y, z)       | Expected Behavior            |
|------|---------------------------------|------------------------|------------------------------|
| 1    | Typical reachable point         | (10, 5, -10)           | Returns valid angles         |
| 2    | Very close to base              | (1, 1, -2)             | Returns valid small angles   |
| 3    | Near maximum reach              | (25, 0, -5)            | Returns valid angles         |
| 4    | Unreachable point               | (35, 10, 0)            | Returns unreachable warning  |
| 5    | Large negative Z                | (5, 5, -30)            | Returns valid large angles   |

##  Code Testing Function

A dedicated test function runs these 5 cases and prints:
- Target coordinates
- Calculated joint angles (if reachable)
- A message indicating reachability

