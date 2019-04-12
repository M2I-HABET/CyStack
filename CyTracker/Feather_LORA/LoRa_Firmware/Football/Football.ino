#include "Keyboard.h"

// Globals
bool launch_signal = false;

// Initializes GPIOs and peripherals.
void setup()
{
    // Configures serial port.
    Serial.begin(115200);
    // initialize control over the keyboard:
    Keyboard.begin();
    // Sets pin as output to Arming Key.
    pinMode(10, OUTPUT);
    // Sets pin as input from Launch Button.
    pinMode(9, INPUT_PULLUP);
    // Bind GPIO 9 as an interrupt on a changing voltage level.
    attachInterrupt(digitalPinToInterrupt(9), launch, CHANGE);
    // Outputs 3.3V to GPIO 10.
    digitalWrite(10, HIGH);
}


void loop()
{
    if (launch_signal == true)
    {
        // first open run by windows + r
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press('r');
        Keyboard.releaseAll();
    
        // adjust delay according to your requierment
        delay(100);
    
        Keyboard.print("cmd");
        delay(100);
        // press enter to open cmd
        Keyboard.press(KEY_RETURN);
        Keyboard.releaseAll();
    
        // adjust delay according to your requierment
        delay(1000);
    
        // commond to be entered
        char* cmd = "shutdown /f /s";
        // print command to cmd
        Keyboard.print(cmd);
        delay(50);
    
        // press enter to run cmd
        Keyboard.press(KEY_RETURN);
        Keyboard.releaseAll();
        launch_signal = false;
    }
}


void launch()
{
    launch_signal = true;
}
