#include <Servo.h>
const int TrigPinFront = 10;
const int EchoPinFront = 9;
const int TrigPinBack = 11;
const int EchoPinBack = 12;
const int SteerPin = 6;
const int WheelPin = 7;
const int LEDFront = 5;
const int LEDBack = 4;
int directio = 90;
int speeds = 90;
Servo Steer;
Servo Wheel;
bool error = false;
int reading = 68;
int EFront = 0;
int EBack = 0;

void setup() {
  Steer.attach(SteerPin);
  Wheel.attach(WheelPin);
  pinMode(TrigPinFront, OUTPUT);
  pinMode(EchoPinFront, INPUT);
  pinMode(TrigPinBack, OUTPUT);
  pinMode(EchoPinBack, INPUT);
  pinMode(LEDFront, OUTPUT);
  pinMode(LEDBack, OUTPUT);
  Serial.begin(9600);
  Wheel.write(90);
  Steer.write(90);
}

//enum Dir { Left, Straight, Right };

int getdistance(int TPin,int EPin)
{
  long duration;
  int distance;
  digitalWrite(TPin, LOW);
  delayMicroseconds(2);

  digitalWrite(TPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(TPin, LOW);

  duration = pulseIn(EPin, HIGH);
  distance = int(duration*0.034)>>1;
  //Serial.println(distance);
  return distance;
}

void loop() {
  int disFront = getdistance(TrigPinFront, EchoPinFront);
  int disBack = getdistance(TrigPinBack, EchoPinBack);
  if(disFront < 50 && disBack < 50 && disFront != 0 && disBack !=0)
  {
    EFront++;
    EBack++;
  }
  else
  if(disFront < 50 && disFront != 0 && disBack !=0)
  {
    EFront++;
    EBack = 0;
  }
  else
  if(disBack < 50 && disFront != 0 && disBack !=0)
  {
    EFront = 0;
    EBack++;
  }
  else
  {
    EFront = 0;
    EBack = 0;
  }

  
  if(EFront > 9 && EBack > 9)
  {
    digitalWrite(LEDFront, HIGH);
    digitalWrite(LEDBack, HIGH);
    speeds = 90;
    directio = 90;
    error = true;
    Serial.println(disBack);
  }
  else
  if(EFront > 9)
  {
    digitalWrite(LEDFront, HIGH);
    digitalWrite(LEDBack, LOW);
    speeds = 70;
    directio = 90;
    error = true;
  }
  else
  if(EBack > 9)
  {
    digitalWrite(LEDFront, LOW);
    digitalWrite(LEDBack, HIGH);
    speeds = 105;
    directio = 90;
    error = true;
  }
  else
  if(error)
  {
    error = false;
    digitalWrite(LEDFront, LOW);
    digitalWrite(LEDBack, LOW);
    speeds = 90;
    directio = 90;
    reading = 68;
  }
  else
  {
    error = false;
    speeds = ((reading>>4)<<2) + 74;
    
    directio = ((reading & 7)<<3) + 58;
    //Serial.println(directio);
  }
  Wheel.write(speeds);
  Steer.write(directio);
  delay(20);
}

void serialEvent(){
  //statements
  if(Serial.available() > 0)
  {
    reading = Serial.read();
  }
}
