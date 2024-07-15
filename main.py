"""Basic test script for the kRPC API."""

import time
import krpc

### create a connection to the KSP game
conn = krpc.connect(name="Tracker")

vessel = conn.space_center.active_vessel
vessel.control.sas = False
vessel.control.rcs = False

### set up streams for telemetry
roll = conn.add_stream(getattr, vessel.flight(), "roll")
pitch = conn.add_stream(getattr, vessel.flight(), "pitch")
heading = conn.add_stream(getattr, vessel.flight(), "heading")
time.sleep(1)

### first, detumble the satellite
# conn.ui.message("Initiating SAS")
# vessel.control.sas = True

### point towards Earth
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_velocity_reference_frame
ap.target_direction = (0, -1, 0)
conn.ui.message("Trying to point towards Earth")

while vessel.flight().surface_altitude > 300:
    ap.engage()
    ap.wait()
    ap.disengage()
    time.sleep(0.5)
conn.ui.message("So long, and thanks for all the fish")
