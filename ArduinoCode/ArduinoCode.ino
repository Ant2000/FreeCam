#include<Servo.h>

Servo servo1;
Servo servo2;

int pos1 = 90;
int pos2 = 90;
String s1, s2, s1b = "", s2b = "";
char s;
bool flag, newData = false;
const double kh = (tan(29 * M_PI / 180) / 480);
const double kw = (tan(29 * M_PI / 180) / 640);
int b, h, locationW, locationH;
double betaW, betaH;

int intw = 0;
int derw = 0;
float kpw = 0.1;
float kiw = 0;
float kdw = 0;
float errw = 0;

int inth = 0;
int derh = 0;
float kph = 0.1;
float kih = 0;
float kdh = 0;
float errh = 0;

void setup() 
{
  servo1.attach(9);
  servo2.attach(10);
  Serial.begin(9600);
}

void loop() 
{
  while (Serial.available() > 0)
  {
    s1 = "";
    s2 = "";
    flag = false;
    while(true)
    {
      s = Serial.read();
      if(s == '|')
        flag = true;
      else if(s == '\n')
        break;
      else if(flag == false && isAlphaNumeric(s))
        s1 = s1 + s;
      else if(flag == true && isAlphaNumeric(s))
        s2 = s2 + s;
    }
    if(s1 != s1b || s2 != s2b)
      newData = true;
    if(newData == true)
    {
      s1b = s1; s2b = s2;
      newData = false;
      locationW = s1.toInt(); locationH = s2.toInt();
      if(locationH == 700 and locationW == 700)
      {
        servo1.write(90);
        servo2.write(90);
        continue;
      }
      b = abs(locationW - 320); h = abs(locationH - 240);
      betaW = atan(b * kw) * 180 / M_PI; betaH = atan(h * kh) * 180/ M_PI;

      intw = intw + betaW; derw = betaW - errw;
      errw = betaW;
      betaW = (kpw * betaW) + (kiw * intw) + (kdw * derw);

      inth = inth + betaH; derh = betaH - errh;
      errh = betaH;
      betaH = (kph * betaH) + (kih * inth) + (kdh * derh);

      if(locationW < 320)
        pos1 = round(pos1 + (betaW  * -1));
      else
        pos1 = round(pos1 + betaW);
      if(locationH < 240)
        pos2 = round(pos2 + (betaH * -1));
      else
        pos2 = round(pos2 + betaH);

      /*Serial.print(betaW * 100);
      Serial.print("\t");
      Serial.println(betaH * 100);*/

      if(pos1 < 0)
        pos1 = 0;
      else if(pos1 > 180)
        pos1 = 180;

      if(pos2 < 0)
        pos2 = 0;
      else if(pos2 > 180)
        pos2 = 180;
      servo1.write(pos1);
      servo2.write(pos2);
      /*Serial.print(pos1);
      Serial.print("\t");
      Serial.println(pos2);*/
    }
  }
}
