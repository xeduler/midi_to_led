#define PIN_R 5
#define PIN_G 6
#define PIN_B 3

#define SPEED 0.001
#define BRIGHTNESS 127

char mode = 0;
char r, g, b = 0;

float now;

void setup(){
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);

  digitalWrite(PIN_R, LOW);
  digitalWrite(PIN_G, LOW);
  digitalWrite(PIN_B, LOW);

  Serial.begin(115200);
}





void loop(){
  if(Serial.available() >= 4){
    
    b = Serial.read();
    r = Serial.read();
    g = Serial.read();
    mode = Serial.read();

    if(mode == 1){
      set(r, g, b);
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

    set(r, g, b);
  }
}




void set(char r, char g, char b){
  analogWrite(PIN_R, r);
  analogWrite(PIN_G, g);
  analogWrite(PIN_B, b);
}
