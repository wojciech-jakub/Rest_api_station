
#include <DHT.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <BH1750.h>


#define DHT22PIN 7    
#define DHT11PIN 8     
#define DHTTYPE DHT22   

Adafruit_BMP280 bme; 
BH1750 lightMeter(0x23);
DHT dht22(DHT22PIN, DHTTYPE);



float temperatura ;

struct IMU_data {
  float temperatura;
  float atlitude;
  float hum22;
  float temp22;
  float bmptemp;
  float lux;
  float bmppressure;
  
};

IMU_data IMU_data_holder;

int len_struct = sizeof(IMU_data_holder);
void send_IMU_struct() {
  Serial.write('S');
  Serial.write((uint8_t *)&IMU_data_holder, len_struct);
  Serial.write('E');
  return;
}


void set_IMU_data(float temperatura, float atlitude, float hum22, float temp22, float bmptemp, float bmppressure, float lux) {
  IMU_data_holder.temperatura = temperatura;
  IMU_data_holder.atlitude = atlitude;
  IMU_data_holder.hum22 = hum22;
  IMU_data_holder.temp22 = temp22;
  IMU_data_holder.bmptemp = bmptemp;
  IMU_data_holder.bmppressure = bmppressure;
  IMU_data_holder.lux = lux;
}

void setup()
{
  Serial.begin(9600);
  //  dht11.begin();
  dht22.begin();
  Wire.begin();
  
  Serial.print(F("size of struct: "));
  Serial.print(len_struct);
  Serial.println();
  
  if (!bme.begin(0x76)) {  
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println(F("BH1750 Advanced begin"));
  }
}
void loop() {

    temperatura = analogRead(0);
    temperatura = temperatura * 0.48828125;

    set_IMU_data(temperatura, bme.readAltitude(1028.00), dht22.readHumidity(),
                 dht22.readTemperature(),bme.readTemperature(), bme.readPressure(),
                 lightMeter.readLightLevel());

    send_IMU_struct();

}

