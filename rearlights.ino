#define RED1_LED 11
#define RED2_LED 10
#define WHITE1_LED 9
#define RED3_LED 4
#define RED4_LED 3
#define WHITE2_LED 2

int brightness = 255;

int r1Bright = 0;
int r2Bright = 0;
int w1Bright = 0;
int r3Bright = 0;
int r4Bright = 0;
int w2Bright = 0;

int fadeSpeed = 1000;

void setup() {
  // put your setup code here, to run once:
pinMode(RED1_LED, OUTPUT);
pinMode(RED2_LED, OUTPUT);
pinMode(WHITE1_LED, OUTPUT);
pinMode(RED3_LED, OUTPUT);
pinMode(RED4_LED, OUTPUT);
pinMode(WHITE2_LED, OUTPUT);

TurnOn();
delay(500);
TurnOff();
}

void TurnOn() { 
  for (int i = 0; i < 256; i++) {
    analogWrite(RED1_LED, r1Bright);
    r1Bright += 1;
//    delay(fadeSpeed);
    }

  for (int i = 0; i < 256; i++) {
    analogWrite(RED2_LED, r2Bright);
    r2Bright += 1;
//    delay(fadeSpeed);
    }
    
  for (int i = 0; i < 256; i++) {
    analogWrite(WHITE1_LED, w1Bright);
    w1Bright += 1;
//    delay(fadeSpeed);
    }

  for (int i = 0; i < 256; i++) {
    analogWrite(RED3_LED, r3Bright);
    r3Bright += 1;
//    delay(fadeSpeed);
    }

  for (int i = 0; i < 256; i++) {
    analogWrite(RED4_LED, r4Bright);
    r4Bright += 1;
//    delay(fadeSpeed);
    }

  for (int i = 0; i < 256; i++) {
    analogWrite(WHITE2_LED, w2Bright);
    w2Bright += 1;
//    delay(fadeSpeed);
    }
  }

void TurnOff() {
  for (int i = 0; i < 256; i++) {
    analogWrite(RED1_LED, brightness);
    analogWrite(RED2_LED, brightness);
    analogWrite(WHITE1_LED, brightness);
    analogWrite(RED3_LED, brightness);
    analogWrite(RED4_LED, brightness);
    analogWrite(WHITE2_LED, brightness);
    brightness -= 1;
    delay(fadeSpeed);
    }
  }

void loop() {
  // put your main code here, to run repeatedly:

}
