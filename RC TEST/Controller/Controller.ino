const int X_Pin = 0;
const int Y_Pin = 1;
void setup() {
  Serial.begin(9600);
}
int state = 0;
void loop() {
  // put your main code here, to run repeatedly:
  int x, y;
  //btnState = digitalRead(btnPin); this is a ok code
  x = analogRead(X_Pin);
  y = analogRead(Y_Pin);
  x = -(((x+128)>>7) - 8);
  y = (y+128)>>7;
  byte a = x + (y<<4);
  /*Serial.print("x: ");
  Serial.println(x);
  Serial.print("y: ");*/
  //Serial.println(x);
  Serial.write(a);
}
