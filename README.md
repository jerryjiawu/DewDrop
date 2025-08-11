## DewDrop: A cheap and accessible weather station for vulnerable communities
DewDrop is a low-cost, solar-powered weather station designed to provide critical environmental data to communities vulnerable to climate change. It features temperature, pressure, and rain detection capabilities, and uses LoRa technology for long-range communication.

### How to Use
3D print the provided STL files to create the DewDrop casing. Once assembled, deploy the station in a suitable location with good solar exposure.

### Running the Code
1. Clone the repository.
   ```bash
   git clone https://github.com/jerryjiawu/DewDrop
   ```
2. Navigate to the project directory.
   ```bash
   cd DewDrop
   ```
3. Open the Arduino IDE and load the `Station.ino` to program the weather station. To program the reciver, load the `Receiver.ino` file.
   - Ensure you have the correct board selected in the Arduino IDE (Heltec ESP32 V2).
   - Set the correct COM port for your device.
   - Upload the code to the board.
4. Connect the Heltec ESP32 V2 board to your computer.
5. Install the required libraries:
   - `LoRa`
   - `Wire`
   - `Adafruit_BMP085`
   - `heltec`
6. Compile and upload the code to the board.
7. Run the app
  pip install -r requirements.txt
8. Start the app
   ```bash
   python app.py
   ```

#### Cost Breakdown

| Component                         | Cost (CAD) |
|-----------------------------------|------------|
| 30g PLA (~$0.20/g)                | $6.00      |
| Heltec ESP32 V2                   | $25.50     |
| Screws                            | $0.50      |
| Wires                             | $0.20      |
| Capacitive Moisture Sensor v1.2   | $4.50      |
| BMP-180                           | $2.85      |
| 5V Buck Converter                 | $5.00      |
| 5W Solar Panel                    | $20.00     |
| **Total (USD)**                   | **$46.92** |

#### Key Features

- Temperature, pressure, and rain detection
- Long-distance IoT (10+ km line of sight)
- Mesh networking (future implementation)
- Solar powered, self-sustaining
- Simple deployment and operation

### Design Criteria

DewDrop was developed with the following goals:

- **Easy deployment in inaccessible areas:** Designed for locations where infrastructure is limited, such as mountain ranges.
- **Self-sustaining operation:** Powered by solar energy and long-range LoRa radios, requiring no external infrastructure.
- **Affordability and scalability:** Low-cost and easy to assemble, enabling widespread deployment for more effective weather monitoring.

The ESP32 LoRa microcontroller was chosen for its balance of cost and capability, and modular 3D-printed casings allow customization for different sensor needs (e.g., moisture sensors for flood-prone areas, temperature sensors for heatwaves).

### Why This Matters

Addressing climate change requires more than policy changes; it demands practical support for those most affected. By providing accessible tools like DewDrop, we can help reduce environmental inequality and give all communities a better chance to adapt to increasing climate risks.
