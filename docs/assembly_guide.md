# Weather Station Assembly Guide

*Complete hardware and electronics assembly instructions for the Observatory Weather Station*

![Assembly Overview](images/assembly-overview.png)
*[Image suggestion: Photo showing all components laid out before assembly]*

## Bill of Materials

### 3D Printed Parts
- 1x Base
- 1x Roof  
- 1x Sensor Holder
- 4x Stevenson Screen panels
- 1x Rotor
- 1x Rotor Cap
- 3x Cup (anemometer cups)
- 12x Tall spacer
- 3x Short spacer

### Hardware Components
- 1x ISO 4018 M8 x 16 Steel hex head screw
- 1x JIS B 1180 M8 x 16 Steel hex head bolt
- 3x JIS B 1185 M4 Steel wing nuts
- 3x Steel rod M4 (10cm length)
- 1x Ball bearing (2349K744 permanently lubricated)
- 3x Neodymium magnets (5x5mm)

### Electronics
- 1x Raspberry Pi Pico
- 1x BMP280 pressure/temperature sensor
- 1x Hall effect sensor (for wind speed detection)
- Jumper wires and breadboard (for prototyping)
- MicroUSB cable for programming
- Weatherproof enclosure for electronics

## Tools Required
- 3D printer (PLA or PETG recommended)
- Soldering iron and solder
- Wire strippers
- Small screwdriver set
- Drill with small bits
- Multimeter (for testing)

![Tools Required](images/tools-required.jpg)
*[Image suggestion: Photo of all required tools arranged on workbench]*

## Assembly Instructions

### Step 1: 3D Print All Components

![3D Printing Setup](images/3d-printing-setup.jpg)
*[Image suggestion: Screenshot of parts arranged on printer bed in slicer software]*

Print settings:
- Layer height: 0.2mm
- Infill: 20-25%
- Support: Only for overhangs >45°
- Material: PETG recommended for outdoor durability

**Print Order Priority:**
1. Base and Roof (main structure)
2. Sensor Holder
3. Stevenson Screen panels
4. Anemometer components (Rotor, Cups, spacers)

### Step 2: Prepare the Base Assembly

![Base Assembly](images/base-assembly-step1.jpg)
*[Image suggestion: Photo showing base component with bearing installation location marked]*

1. **Install the main bearing**:
   - Press the ball bearing into the center hole of the Base
   - Ensure it sits flush and rotates smoothly

![Bearing Installation](images/bearing-installation.jpg)
*[Image suggestion: Close-up photo of bearing being pressed into base]*

2. **Mount the Sensor Holder**:
   - Secure the Sensor Holder to the Base using appropriate mounting points
   - This will house the BMP280 sensor

![Sensor Holder Mounting](images/sensor-holder-mount.jpg)
*[Image suggestion: Photo showing sensor holder attached to base]*

### Step 3: Build the Stevenson Screen

![Stevenson Screen Assembly](images/stevenson-screen-assembly.jpg)
*[Image suggestion: Exploded view diagram showing how the 4 panels connect]*

The Stevenson Screen provides radiation shielding for accurate temperature readings.

1. **Assemble the ventilation panels**:
   - Connect the 4 Stevenson Screen panels to form a protective enclosure
   - Ensure adequate ventilation gaps between panels
   - Mount around the Sensor Holder

2. **Secure with hardware**:
   - Use M4 wing nuts for easy maintenance access
   - Ensure all panels are properly aligned

### Step 4: Construct the Anemometer

![Anemometer Exploded View](images/anemometer-exploded.jpg)
*[Image suggestion: Technical diagram showing rotor, rods, cups, and magnets in exploded view]*

1. **Prepare the rotor assembly**:
   - Insert the 3 steel rods (M4, 10cm) into the Rotor at 120° intervals
   - Secure with appropriate fasteners

![Rotor Assembly](images/rotor-assembly.jpg)
*[Image suggestion: Photo showing rotor with 3 rods inserted at 120° spacing]*

2. **Attach the cups**:
   - Mount one Cup to each steel rod using the short spacers
   - Ensure cups are oriented correctly for wind capture
   - All cups should face the same rotational direction

![Cup Orientation](images/cup-orientation-diagram.png)
*[Image suggestion: Top-down diagram showing correct cup orientation for wind capture]*

3. **Install magnets for wind speed sensing**:
   - Embed the 3 neodymium magnets (5x5mm) into the Rotor
   - Space them evenly at 120° intervals
   - Ensure magnets are flush with the rotor surface

![Magnet Installation](images/magnet-installation.jpg)
*[Image suggestion: Close-up photo of magnets being installed in rotor, with diagram showing 120° spacing]*

4. **Complete the rotor assembly**:
   - Cap the rotor with the Rotor Cap
   - Mount the complete assembly to the Base using the M8 hex head screw
   - Ensure smooth rotation with minimal friction

![Complete Anemometer](images/complete-anemometer.jpg)
*[Image suggestion: Photo of fully assembled anemometer mounted on base]*

### Step 5: Electronics Assembly

![Electronics Wiring Diagram](images/electronics-wiring-diagram.png)
*[Image suggestion: Clean schematic diagram showing Pi Pico connections to BMP280 and Hall sensor]*

1. **Prepare the Raspberry Pi Pico**:
   - Install MicroPython or CircuitPython firmware
   - Test basic functionality before installation

![Pi Pico Setup](images/pi-pico-setup.jpg)
*[Image suggestion: Photo of Pi Pico connected to computer for initial setup]*

2. **Connect the BMP280 sensor**:
   ```
   BMP280 -> Pi Pico
   VCC    -> 3.3V
   GND    -> GND
   SCL    -> GP1 (I2C)
   SDA    -> GP0 (I2C)
   ```

![BMP280 Wiring](images/bmp280-wiring.jpg)
*[Image suggestion: Photo showing BMP280 sensor wired to Pi Pico with colored wires]*

3. **Wire the Hall effect sensor**:
   ```
   Hall Sensor -> Pi Pico
   VCC        -> 3.3V
   GND        -> GND
   OUT        -> GP2 (Digital input)
   ```

![Hall Sensor Wiring](images/hall-sensor-wiring.jpg)
*[Image suggestion: Photo of Hall effect sensor with wiring connections clearly visible]*

4. **Position the Hall effect sensor**:
   - Mount the sensor near the rotor magnet path
   - Ensure it detects magnet passes without interference
   - Test rotation detection before final assembly

![Hall Sensor Positioning](images/hall-sensor-positioning.jpg)
*[Image suggestion: Photo showing Hall sensor positioned relative to rotating magnet path]*

### Step 6: Final Assembly

![Final Assembly Steps](images/final-assembly-sequence.jpg)
*[Image suggestion: Series of 3-4 photos showing the final assembly sequence]*

1. **Install the roof**:
   - Secure the Roof to the top of the assembly
   - Use the M8 hex head bolt for main structural connection
   - Ensure weather protection for all components

2. **Electronics housing**:
   - Place the Pi Pico and sensors in weatherproof enclosure
   - Ensure all connections are secure and protected
   - Mount electronics enclosure to the Base

![Electronics Enclosure](images/electronics-enclosure.jpg)
*[Image suggestion: Photo of weatherproof enclosure with Pi Pico and sensors inside]*

3. **Calibration check**:
   - Test anemometer rotation (should spin freely)
   - Verify Hall effect sensor triggers with each magnet pass
   - Check BMP280 readings for reasonable values

### Step 7: Testing and Verification

![Testing Setup](images/testing-setup.jpg)
*[Image suggestion: Photo of completed weather station connected to laptop for testing]*

1. **Mechanical tests**:
   - Verify smooth anemometer rotation
   - Check all fasteners are secure
   - Ensure Stevenson Screen ventilation is unobstructed

2. **Electronic tests**:
   - Test wind speed detection (3 pulses per rotation)
   - Verify temperature and pressure readings
   - Check data logging functionality

3. **Weatherproofing**:
   - Ensure all electronic connections are protected
   - Verify drainage paths in case of water intrusion
   - Test in simulated weather conditions if possible

## Troubleshooting

![Troubleshooting Guide](images/troubleshooting-flowchart.png)
*[Image suggestion: Flowchart diagram showing common problems and solutions]*

### Common Issues:

**Anemometer not rotating smoothly**:
- Check bearing installation
- Verify rotor balance
- Ensure no interference from wiring

**Inconsistent wind speed readings**:
- Verify Hall sensor positioning
- Check magnet alignment
- Test sensor sensitivity

**BMP280 not responding**:
- Check I2C connections
- Verify power supply voltage
- Test with simple I2C scanner code

## Maintenance Notes

![Maintenance Schedule](images/maintenance-schedule.png)
*[Image suggestion: Visual calendar/schedule showing maintenance tasks and frequencies]*

- **Monthly**: Check anemometer rotation and clean if necessary
- **Quarterly**: Verify all fasteners remain tight
- **Annually**: Re-calibrate sensors and check weatherproofing

## Next Steps

Once assembly is complete, proceed to the [Software Setup Guide](software-setup.md) for firmware installation and configuration.

---

## Image and Diagram Suggestions

### Photos You Can Take:
1. **Assembly Overview**: All components laid out before assembly
2. **Tools Required**: All tools arranged on workbench
3. **3D Printing Setup**: Screenshot of parts arranged in slicer software
4. **Step-by-step Assembly Photos**: 
   - Base with bearing installation location marked
   - Bearing being pressed into base
   - Sensor holder mounted to base
   - Rotor with 3 rods inserted at 120° spacing
   - Complete anemometer mounted on base
   - Pi Pico connected to computer for setup
   - BMP280 sensor wired to Pi Pico
   - Hall sensor with wiring connections
   - Hall sensor positioned relative to magnet path
   - Weatherproof enclosure with electronics inside
   - Final assembly sequence (3-4 photos)
   - Completed weather station connected to laptop

### Diagrams You Can Create:
1. **Stevenson Screen Assembly**: Exploded view showing how 4 panels connect
2. **Anemometer Exploded View**: Technical diagram showing all components
3. **Cup Orientation Diagram**: Top-down view showing correct cup positioning
4. **Magnet Installation Diagram**: Shows 120° spacing with measurements
5. **Electronics Wiring Diagram**: Clean schematic of Pi Pico connections
6. **Troubleshooting Flowchart**: Decision tree for common problems
7. **Maintenance Schedule**: Visual calendar showing tasks and frequencies

### CAD Renderings You Can Generate:
- 3D rendered assembly views
- Cross-section views showing internal components
- Detailed component drawings with dimensions
- Animation sequences showing assembly steps

### Tools for Creating Diagrams:
- **Fritzing**: For electronics schematics and breadboard layouts
- **KiCad**: For professional PCB schematics
- **Inkscape/Illustrator**: For technical illustrations
- **Your CAD Software**: For 3D renderings and exploded views
- **Draw.io**: For flowcharts and process diagrams