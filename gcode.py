# TODO useful values
temp = 240  # °C
travel_speed = 1500  # mm / min
penetration_speed = 500  # mm / min
retraction_speed = 800  # mm / min
travel_height = 0.6  # mm
gauge_height = 0.1  # mm (piece of paper)


def generate_gcode(dots):
    preamble = f"""
        G21 ; millimeter
        M0 move tool to origin above {gauge_height}mm feeler gauge and press button to continue

        M17 X Y Z ; enable power to x y z steppers
        G91 ; relative positioning
        G0 F{penetration_speed} Z{-gauge_height}
        G92 ; set origin to current position
        G90 ; absolute positioning
        
        G0 F{retraction_speed} Z10
        M109 R{temp} ; wait for hotend temperature
        G4 S5 ; wait for temperature to equalize
    """

    moves = "".join(
        [
            f"""
                G0 F{travel_speed} X{x} Y{y}
                G1 F{penetration_speed} Z{-z}
                G1 F{retraction_speed} Z{travel_height}
            """
            for (x, y, z) in dots
        ]
    )

    end = f"""
        G0 F{retraction_speed} Z30
    """

    gcode = preamble + moves + end
    pretty = "\n".join([line.strip() for line in gcode.splitlines()])
    return pretty
