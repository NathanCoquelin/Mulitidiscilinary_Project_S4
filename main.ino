// C++ code
//
//int potentiometer = A0;
int led = 3;
float voltage;
//int input;

void setup(){ 
	Serial.begin(9600);
	pinMode(led, OUTPUT);
}

void loop()
{
//  input = analogRead(potentiometer);
//  float output = map(input, 0, 1023, 0, 255);
//  analogWrite(led, output);
//  voltage=(output/256.0)*5;
//  Serial.println(output);
    for (int i = 0; i <= 255; i++){
        analogWrite(led, i);
        delay(10);
    }
    for (int i = 255; i > 0 ; i--){
    analogWrite(led, i);
    delay(10);
  }
}

