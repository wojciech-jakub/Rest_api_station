
#include <DHT.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <BH1750.h>




#define DHT22PIN 7   
#define DHT11PIN 8     
#define DHTTYPE DHT22  
 
//DHT dht11(DHT11PIN, DHTTYPE); 
Adafruit_BMP280 bme;
BH1750 lightMeter(0x23);
DHT dht22(DHT22PIN, DHTTYPE);



unsigned long start_time;
unsigned long end_time;

float temperatura ;
float atlitude;
float hum22;  
float temp22; 
float hum11;  
float temp11; 
float bmptemp;
float lux;
float pressure;


struct IMU_data {
  float time_meassure;
};

// instanciate one struct
IMU_data IMU_data_holder;

int len_struct = sizeof(IMU_data_holder);
void send_IMU_struct() {
  Serial.write('S');
  Serial.write((uint8_t *)&IMU_data_holder, len_struct);
  Serial.write('E');
  return;
}


void set_IMU_data(float time_) {
  IMU_data_holder.time_meassure = time_;
}
void setup()
{
  Serial.begin(9600);
//  dht11.begin();
  Wire.begin();
    Serial.print(F("size of struct: "));
  Serial.print(len_struct);
  Serial.println();
    dht22.begin();

  if (!bme.begin(0x76)) {  
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println(F("BH1750 Advanced begin"));
  }
}
void loop() {

    start_time = micros();
    
    temperatura = analogRead(0);
//  temperatura = temperatura * 0.48828125; 
    atlitude = bme.readAltitude(1028.00);
    hum22 = dht22.readHumidity();
    temp22 = dht22.readTemperature(); 
    bmptemp = bme.readTemperature();
    pressure = bme.readPressure();
    lux = lightMeter.readLightLevel();
    end_time = micros();
    
    set_IMU_data(end_time - start_time);

    send_IMU_struct();
    
}

 
