#define PIN_R 5
#define PIN_G 6
#define PIN_B 3
#define PIN_CEILING 9
#define PIN_WIND 10
#define PIN_UV 11

#define SPEED 0.001
#define BRIGHTNESS 127

char mode = 0;
char r, g, b, ceiling, wind, uv = 0;

float now;

void setup(){
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  pinMode(PIN_CEILING, OUTPUT);
  pinMode(PIN_WIND, OUTPUT);
  pinMode(PIN_UV, OUTPUT);

  digitalWrite(PIN_R, LOW);
  digitalWrite(PIN_G, LOW);
  digitalWrite(PIN_B, LOW);
  digitalWrite(PIN_CEILING, LOW);
  digitalWrite(PIN_WIND, LOW);
  digitalWrite(PIN_UV, LOW);

  Serial.begin(115200);
}





void loop(){
  if(Serial.available() >= 5){
    
    ceiling = Serial.read();
    b = Serial.read();
    r = Serial.read();
    g = Serial.read();
    mode = Serial.read();

    if(mode == 1){
      set(r, g, b, ceiling, wind, uv);
    }
    //Serial.print(r);
    //Serial.print(g);
    //Serial.print(b);
  }
  
  if(mode == 0){
    now = millis() * SPEED;
    r = (sin(now) + 1.0) * BRIGHTNESS;
    g = (sin(now + 2.0943951) + 1.0) * BRIGHTNESS;
    b = (sin(now + 4.1887902) + 1.0) * BRIGHTNESS;

    set(r, g, b, r, 0, r);
  }
}




void set(char r, char g, char b, char ceiling, char wind, char uv){
  analogWrite(PIN_R, r);
  analogWrite(PIN_G, g);
  analogWrite(PIN_B, b);
  analogWrite(PIN_CEILING, ceiling);
  analogWrite(PIN_WIND, wind);
  analogWrite(PIN_UV, uv);
}
