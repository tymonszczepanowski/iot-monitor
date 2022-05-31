const int trigPin = 3;
const int echoPin = 2;

void setup() {
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);

}

int distance = 0;

int frame = 0;

void loop() {

  distance = getSensorDistance();
  
  Serial.println(distance);

  delay(100);

  if(frame%5 == 0){  
    Serial.flush();
    frame = 0;
  }

  frame++;
  
}

int getSensorDistance(){

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);

  int distance = duration * 0.034 / 2;

  return distance;
  
}
