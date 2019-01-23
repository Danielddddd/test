nclude <ESP8266WiFi.h>
#include <Servo.h>


const char* ssid = "IT 404";
const char* password = "bitc5600";

WiFiServer server(80);

int LED_pin = 16;
int turn_on = 0;
int turn_off = 1;

int servoPin = 5;

Servo servo;

int angle = 0;

#include "pitches.h"

int melody[] = {NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4};

int noteDurations[] = {4, 8, 8, 4, 4, 4, 4, 4};

void setup()
{
	Serial.begin(115200);

	delay(10);
	servo.attach(servoPin);
	pinMode(LED_pin, OUTPUT);
	digitalWrite(LED_pin, turn_off);

	Serial.println();
	Serial.println();
	Serial.print("Connecting to ");
	Serial.println(ssid);

	WiFi.begin(ssid, password);

	while (WiFi.status() != WL_CONNECTED)
	{
		delay(500);
		Serial.print(".");
	}

	Serial.println("");
	Serial.println("WiFi connected");

	server.begin();

	Serial.println("Server started");
	Serial.print("Use this URL to connect: ");
	Serial.print("http://");
	Serial.print(WiFi.localIP());
	Serial.println("/");
}

void loop()
{
	WiFiClient client = server.available();

	if (!client)
	{
		return;
	}

	Serial.println("new client");

	while(!client.available())
	{
		delay(1);
	}

	String request = client.readStringUntil('\r');
	Serial.println(request);
	client.flush();

	int value = turn_off;

	if (request.indexOf("/MORTOR=ON") != -1)
	{
		for(angle = 0; angle < 180; angle++) // scan from 0 to 180 degrees
		{ 
			servo.write(angle); 
			delay(30);
			printf("servo 1cycle"); 
		}

		for(angle = 540; angle > 0; angle--) // now scan back from 180 to 0 degree 
		{
			servo.write(angle); 
			delay(30); 
			printf("servo 2cycle"); 
		}
		for (int thisNote = 0; thisNote < 8; thisNote++) 
		{
			int noteDuration = 1000 / noteDurations[thisNote];
			tone(4, melody[thisNote], noteDuration);
			int pauseBetweenNotes = noteDuration * 1.30;
			delay(pauseBetweenNotes);
			noTone(4);
			printf("boser on");
		}
		value == turn_on;
	}

	if (request.indexOf("/LED=ON") != -1)
	{
		digitalWrite(LED_pin, turn_on);
		value = turn_on;
		printf("LED ON");
	}

	if (request.indexOf("/LED=OFF") != -1)
	{
		digitalWrite(LED_pin, turn_off);
		value = turn_off;
		printf("LED OFF");
	}


	client.println("HTTP/1.1 200 OK");
	client.println("Content-Type: text/html");
	client.println(""); //  do not forget this one
	client.println("<!DOCTYPE HTML>");
	client.println("<html>");

	client.print("Dog care system: ");

	if(value == turn_on)
	{
		client.print("ON");
	}

	else
	{
		client.print("OFF");
	}

	client.println("<br><br>");
	client.println("<a href=\"/MORTOR=ON\"\"><button>Servo moter on </button></a>");
	client.println("<a href=\"/LED=ON\"\"><button>LED ON </button></a><br />");
	client.println("<a href=\"/LED=OFF\"\"><button>LED OFF </button></a><br />"); 
	client.println("</html>");

	delay(1);


	Serial.println("Client disonnected");
	Serial.println("");
}
