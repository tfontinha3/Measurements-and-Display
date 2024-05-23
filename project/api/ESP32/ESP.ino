// Define the pins connected to the IR sensor
const int analogPin = 36; // GPIO36 (VP)
const int digitalPin = 27; // GPIO27

// Variables to store pulse count and time
volatile int pulseCount = 0;
unsigned long previousMillis = 0;
const unsigned long interval = 1000; // 0.01 second interval for RPM calculation

// Array to store RPM values and timestamps
const int maxMeasurements = 100; // Adjust size as needed
struct Measurement {
  unsigned long time;
  int rpm;
};
Measurement measurements[maxMeasurements];
int measurementIndex = 0;

void IRAM_ATTR countPulse() {
  pulseCount++;
}

void setup() {
  // Initialize the serial communication
  Serial.begin(115200);

  // Set the digital pin as input and attach interrupt
  pinMode(digitalPin, INPUT);
  attachInterrupt(digitalPin, countPulse, RISING);
}

void loop() {
  // Read the analog value from the sensor
  int analogValue = analogRead(analogPin);

  // Get current time
  unsigned long currentMillis = millis();

  // Calculate RPM every interval
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Calculate RPM (since 20 pulses = 1 rotation)
    int rpm = (pulseCount * 6000 / 20); // Convert pulses per 0.01 second to RPM
    pulseCount = 0; // Reset pulse count for the next interval

    // Save RPM and timestamp in the array
    if (measurementIndex < maxMeasurements) {
      measurements[measurementIndex].time = currentMillis;
      measurements[measurementIndex].rpm = rpm;
      measurementIndex++;
    }
  }
}
