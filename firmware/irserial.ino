#include <IRLibSendBase.h>
#include <IRLib_HashRaw.h>
#include <OneWire.h>

// IR led should be connected to pin 9 on Leonardo
const int PIN_TEMPERATURE_SENSOR = 7;

const int RESULT_OK = 0;
const int RESULT_ERROR_GENERIC = 0xFF;
const int RESULT_ERROR_FREQUENCY = 0xFE;
const int RESULT_ERROR_LEN = 0xFD;
const int RESULT_ERROR_PERIOD = 0xFC;

const int COMMAND_IR = 0;
const int COMMAND_TEMP = 1;

IRsendRaw irsend;
OneWire temp_sensor(PIN_TEMPERATURE_SENSOR);

byte temp_sensor_address[8];

void setup() {
  Serial.begin(9600);

  temp_sensor.reset_search();
  temp_sensor.search(temp_sensor_address);
  byte conf[] = {
    0b00000000,
    0b00000000,
    0b00011111
  };
  temp_sensor.reset();
  temp_sensor.select(temp_sensor_address);
  temp_sensor.write(0x4E);
  temp_sensor.write_bytes(conf, 3);
  delay(1000);
}

void loop() {
  if(Serial.available() == 0) {
    return;
  }
  int command = Serial.read();
  switch(command) {
    case COMMAND_IR:
      execute_ir();
      break;
    case COMMAND_TEMP:
      measure_temp();
      break;
    default:
      return;    
  }
}

void execute_ir() {
  int frequency = Serial.read();
  if(frequency <= 0) {
    while(Serial.available()) Serial.read();
    Serial.write(RESULT_ERROR_FREQUENCY);
    delay(3000);
    return;
  }
  int data_length = Serial.read();
  data_length |= Serial.read() << 8;
  if(data_length <= 0) {
    while(Serial.available()) Serial.read();
    Serial.write(RESULT_ERROR_LEN);
    delay(3000);
    return;
  }
  unsigned int * periods = (unsigned int*)malloc(sizeof(unsigned int) * data_length);
  for(int i = 0; i < data_length; ++i) {
    periods[i] = Serial.read();
    periods[i] |= Serial.read() << 8;
    if(periods[i] <= 0) {
      while(Serial.available()) Serial.read();
      Serial.write(RESULT_ERROR_PERIOD);
      delay(3000);
      return;
    }
  }
  irsend.send(periods, data_length, frequency);
  free(periods);
  Serial.write(RESULT_OK);
}

void measure_temp() {
  temp_sensor.reset();
  temp_sensor.select(temp_sensor_address);
  temp_sensor.write(0x44, 1);
  delay(1000);
  temp_sensor.reset();
  temp_sensor.select(temp_sensor_address);
  temp_sensor.write(0xBE);
  byte data[9];
  for(int i = 0; i < 9; ++i) {
    data[i] = temp_sensor.read();
  }
  Serial.write(RESULT_OK);
  Serial.write(data[0]);
  Serial.write(data[1]);
}

