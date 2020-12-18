#define BUTTON1 9
#define BUTTON2 8
#define LED1 6
#define LED2 7

int current = 1;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON1, INPUT);
  pinMode(BUTTON2, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  
  // Figure out which monitor is being used currently
  while(!Serial.available()){}
  String s = Serial.readString();
  current = s.toInt();
  
  if (current == 1) 
    digitalWrite(LED1, HIGH);
  else if (current == 2)
    digitalWrite(LED2, HIGH);
}

void loop() {
  int pressed1 = digitalRead(BUTTON1);
  int pressed2 = digitalRead(BUTTON2);

  // Maybe not necessary
  if (Serial.available()) {
    String s = Serial.readString();
    if (s.length() != 0) {
      current = s.toInt();
      if (current == 1) {
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
      }
      else if (current == 2) {
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
      }
    }
  }
  
  if (pressed1 && current != 1) {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, LOW);
    Serial.println("1");
    current = 1;
    while(digitalRead(BUTTON1) || digitalRead(BUTTON2)) {
    
    }
  }
  else if (pressed2 && current != 2) {
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, HIGH);
    Serial.println("2");
    current = 2;
    while(digitalRead(BUTTON1) || digitalRead(BUTTON2)) {
    
    }
  }
}
