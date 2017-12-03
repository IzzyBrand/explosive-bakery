#include "HX711.h"

HX711 scale;

void setup() {
  Serial.begin(115200);
  Serial.print("Init...\t");
  scale.begin(3, 2);
  Serial.print("Set scale...\t");
  scale.set_scale(279.75);
  Serial.print("Tare...\t");
  scale.tare(100);  
  Serial.println("COMPLETE");
}

void loop() {
  Serial.print(millis());
  Serial.print(",\t");
  Serial.println(scale.get_units(200));
}
