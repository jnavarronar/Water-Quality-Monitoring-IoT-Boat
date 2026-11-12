//Sensor TDS
#include <EEPROM.h>
#include "GravityTDS.h"
#define TdsSensorPin 35
#define EEPROM_SIZE 512
GravityTDS gravityTds;
float temperature = 25, tdsValue;


//Sensor temp
#include <OneWire.h>                
#include <DallasTemperature.h>
OneWire ourWire(4);                //Se establece el pin 2  como bus OneWire
DallasTemperature sensors(&ourWire); 


//Sensor PH
const int potPin=36;
float ph;
float Value=0;


//Thingspeak
#include <WiFi.h>
#include "ThingSpeak.h"
// Wi-Fi credentials and the ThingSpeak channel/key are kept in secrets.h,
// which is not uploaded to GitHub. Copy secrets.example.h to secrets.h and fill it in.
#include "secrets.h"
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
WiFiClient theClient;
unsigned long myChannelNumber = SECRET_CH_ID;
const char myWriteAPIKey[] = SECRET_WRITE_APIKEY;


void setup()
{
    delay(1000);
    Serial.begin(9600);
    sensors.begin();   //Se inicia el sensor

    
    EEPROM.begin(EEPROM_SIZE);  //Initialize EEPROM
    gravityTds.setPin(TdsSensorPin);
    gravityTds.setAref(3.3);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds.setAdcRange(4096);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds.begin();  //initialization


    pinMode(potPin,INPUT);


    ThingSpeak.begin(theClient);
}

void loop()
{
    sensors.requestTemperatures();   //Se envía el comando para leer la temperatura
    float temp= sensors.getTempCByIndex(0); //Se obtiene la temperatura en ºC


    //temperature = readTemperature();  //add your temperature sensor and read it
    gravityTds.setTemperature(temp);  // set the temperature and execute temperature compensation
    gravityTds.update();  //sample and calculate
    tdsValue = gravityTds.getTdsValue();  // then get the value
    Serial.print(tdsValue,0);
    Serial.println("ppm");

    Value= analogRead(potPin);
    float voltage=Value*(3.3/4095.0);
    ph=(3.3*voltage);
    
    Serial.print("Temperatura= ");
    Serial.print(temp);
    Serial.println(" C");
    Serial.print(ph);
    Serial.println("PH");
    delay(1000);


  if(WiFi.status()!=WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(SECRET_SSID);
    while (WiFi.status() != WL_CONNECTED){
        WiFi.begin(ssid,pass);
        Serial.print(".");
        delay(5000);
    }
    Serial.println("\nConnected.");
  }
    ThingSpeak.setField(1,tdsValue);
    ThingSpeak.setField(2,ph);
    ThingSpeak.setField(3,temp);


  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  if (x == 200){
      Serial.println("Channel update successful.");
  }
  else{
      Serial.println("Problem updateing channel.");
  }
  delay(20000);
}
