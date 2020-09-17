#define sensor 3
int for_st = 1;

void setup()
{
    pinMode(sensor, INPUT_PULLUP);
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
}

void loop()
{

    if (digitalRead(sensor) == LOW) { // za pushbutton stavi HIGH
        for_st = 0;
    }

    delay(1);

    if (digitalRead(sensor) == HIGH) { // za pushbutton stavi LOW
        if (for_st == 0) {

            Serial.println('1');
            digitalWrite(13, digitalRead(13) ^ 1);
        }
        for_st = 1;
    }
}
