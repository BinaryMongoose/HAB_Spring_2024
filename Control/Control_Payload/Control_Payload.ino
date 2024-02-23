#include <SPI.h>
#include <SD.h>

#include <Adafruit_BME680.h>
#include <bme68x.h>
#include <bme68x_defs.h>

#define SEALEVELPRESSURE_HPA (1013.25)

File output_file;
Adafruit_BME680 bme; 

// Defning timer periods (milliseconds)
const int FIVE_SECONDS = 5000;
const int TEN_SECONDS  = 10000;

// Runs once on start.
void setup() {
  // Setting up SD card. 
  if (!SD.begin(4)) {
    while (1);
  }

  // Open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  output_file = SD.open("data.csv", FILE_WRITE);

  // Write the header line:
  // Must be consistent with the order which we write the data. 
  output_file.println("temp,hum,pressure,alt,gas_r");

  // Starting the BME 
  if (!bme.begin()) {
    Serial.println("Could not find the BME sensor!");
  }

  // Set up oversampling and filter initialization.
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);  // 320*C for 150 ms
}

// Loops forever
void loop() {
  // If we could get readings from BME && could write to file, 
  // write 1 line to output_file. 
  if (bme.performReading() && output_file) {
    output_file.print(bme.temperature);  output_file.print(",");
    output_file.print(bme.humidity); output_file.print(",");
    output_file.print(bme.pressure); output_file.print(",");
    output_file.print(bme.readAltitude(SEALEVELPRESSURE_HPA)); output_file.print(",");
    output_file.print(bme.gas_resistance);
    output_file.println();
    output_file.flush();
  } else {  // If we could not read data, wirte error to file. 
    output_file.println("Could not read BME sensor. :(");
  }

  // TODO: Wait for 10 seconds
  delay(10); // <- Milliseconds
}