#include <IRLibSendBase.h>
#include <IRLib_HashRaw.h>
// IR led should be connected to pin 9 on Leonardo

const int RESULT_OK = 0;
const int RESULT_ERROR = -1;

IRsendRaw irsend;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() == 0) {
    return;
  }
  int frequency = Serial.read();
  int v = 0;
  int r = Serial.read();
  v |= r;
  r = Serial.read();
  v |= r << 8;
  int len = v;
  if(frequency <= 0 || len <= 0) {
    Serial.write(RESULT_ERROR);
    delay(3000);
    while(Serial.available()) {
      Serial.read();
    }
    return;
  }
  unsigned int * periods = (unsigned int*)malloc(sizeof(unsigned int) * len);
  for(int i = 0; i < len; ++i) {
    v = 0;
    unsigned int r = Serial.read();
    v |= r;
    r = Serial.read();
    v |= r << 8;
    periods[i] = v;
  }
  for(int i = 0; i < len; ++i) {
    if(periods[i] <= 0) {
      Serial.write(RESULT_ERROR);
      return;
    }
  }
  irsend.send(periods, len, frequency);
  free(periods);
  Serial.write(RESULT_OK);
}
