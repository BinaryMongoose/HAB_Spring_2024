#include <SPI.h>
#include <SD.h>

#include <Adafruit_BME680.h>
#include <bme68x.h>
#include <bme68x_defs.h>

#define SEALEVELPRESSURE_HPA (1013.25)

File myFile;
Adafruit_BME680 bme; 

const int FIVE_SECONDS = 5000;
const int TEN_SECONDS  = 10000;

void setup() {
  Serial.begin(9600);  // Setting up Serial

  Serial.print("Initializing SD card...");
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  myFile = SD.open("data.csv", FILE_WRITE);

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

void loop() {
  if (!bme.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }

  if(myFile) {
    myFile.print(bme.temperature);  myFile.print(",");
    myFile.print(bme.humidity); myFile.print(",");
    myFile.print(bme.pressure); myFile.print(",");
    myFile.print(bme.readAltitude(SEALEVELPRESSURE_HPA)); myFile.print(",");
    myFile.print(bme.gas_resistance);
    myFile.println();
    myFile.flush();
  }

  Serial.println();
  delay(10);
}