#include "LiquidCrystal.h" //to find in library

LiquidCrystal lcd(3,5,6,7,8,9,10,11,12,13);


double time1 = 0.0;
double time2 = 0.0;
double totalTime = 0.0;
double distance = 0.7;
double speedRocket = 2.0;
const int pin1 = 2;
const int pin2 = 4;
boolean pin1Passed = false;
boolean pin2Passed = false;
double angle = 3.14159265359/6;
double weight = 0.2;
double gravity = 9.81;
double xFinal = 0.0;
int currentTime;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lcd.begin(16,2);
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
}

void loop() {
  boolean pin1State = digitalRead(pin1);
  boolean pin2State = digitalRead(pin2);
  currentTime = millis();

  if (pin1State == LOW && pin1Passed == false) {
    time1 = currentTime;
    pin1Passed = true;
    Serial.println(time1);
    }
  if (pin2State == HIGH && pin2Passed == false && pin1Passed == true){
    time2 = currentTime;
    pin2Passed = true;
    }
  totalTime = time2 - time1;
  Serial.println(totalTime);
  speedRocket = 1000*distance/totalTime;
  xFinal = sq(speedRocket)*sqrt(2)/2/9.81;
  //speedRocket * cos(angle) * (2 * speedRocket * sin(angle))/(gravity)
  lcd.setCursor(0, 0);
  lcd.write("vel: ");
  lcd.print(speedRocket);
  lcd.write(" m/s      ");
  lcd.setCursor(0, 1);
  lcd.write("dist: ");
  lcd.print(xFinal);
  lcd.write(" m");
  Serial.println(speedRocket);
}
