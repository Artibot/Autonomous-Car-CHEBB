const int X_Pin = 0;
const int Y_Pin = 1;
void setup() {
  Serial.begin(9600);
}
int state = 0;
void loop() {
  // put your main code here, to run repeatedly:
  int x, y;
  //btnState = digitalRead(btnPin);
  x = analogRead(X_Pin);
  y = analogRead(Y_Pin);
  x = x/115;
  y = y/115;
  /*Serial.print("x: ");
  Serial.println(x);
  Serial.print("y: ");
  Serial.println(y);*/
  Serial.write(x + y*10);
}
