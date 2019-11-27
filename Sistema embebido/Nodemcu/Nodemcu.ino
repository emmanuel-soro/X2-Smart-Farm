/****************************************************************************
  --------------------------------------------------------------------------
  | Proyecto      : Smart Farm
  | Actualizado   : 28/09/2019
  | Tema          : Modulo Wifi 
  | Autores       : ~ Frattini, Maximiliano Gabriel (DNI: 26.849.323)
  |                 ~ Rodeiro, Gonzalo (DNI: 37.753.908)
  |                 ~ Salva, Ricardo Nicolás (DNI: 38.142.454)
  |                 ~ Soro, Emmanuel (DNI: 33.778.589)
  --------------------------------------------------------------------------
*****************************************************************************/
#include <ESP8266WiFi.h>

//const char* ssid = "SO Avanzados";
//const char* password = "SOA.2019";
/* Variables de conexion a Red */
const char* ssid = "Telecentro-8b60";
const char* password = "GJZWWNHNMZ4Q";

/* Variables de uso global */
char lastState = 'X';
long int tiempoParaFoto = 600*1000;
long int tiempoMaxParaFoto = 605*1000;

/* Flags de tiempo */
unsigned long startMillis;
unsigned long currentMillis;

/* Web server del mcu */
WiFiServer server(80);

/* Conexion del servidor */
const char* ipServidor = "192.168.30.151";
const uint16_t puertoIpServidor = 8087;
WiFiClient client;

void setup() 
{
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  /* Iniciamos el Servidor web. */
  server.begin();
  /* Mostramos la IP */
  Serial.print("Esta es la IP para conectar: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
  startMillis = millis();
}

bool iniciarCliente()
{
  return client.connect(ipServidor, puertoIpServidor) ? true : false;
}

bool consultarPeticion(WiFiClient client)
{
  String req = client.readStringUntil('\r');
  client.flush();
  if (req.indexOf("/dato?id=F") != -1) 
  {
     Serial.print('F');
     lastState = 'F';
  }
  else if (req.indexOf("/dato?id=R") != -1) 
  {
     Serial.print('R');
     lastState = 'R';
  }
  else if (req.indexOf("/dato?id=T") != -1) 
  {
     Serial.print('T');
     lastState = 'T';
  }
  else if(req.indexOf("/dato?id=W") != -1) 
  {
     Serial.print('W');
     lastState = 'W';
  }
  else
  {
     client.stop();
     return false;
  }
  return true;
}

void tomarImagen(WiFiClient client)
{
  client.print(String("GET /photo")
  + " HTTP/1.1\r\n" + 
  "Host: 192.168.30.151:8087" + "\r\n" + 
  "Connection: keep-alive\r\n" +
  "\r\n"       
  );
  startMillis = millis();
}

void loop() 
{
  if(WiFi.status() != WL_CONNECTED)
  {
     WiFi.begin(ssid, password);
  }
  else
  {
     currentMillis = millis();
     if(currentMillis - startMillis < tiempoParaFoto) 
     {
        WiFiClient client = server.available();
        if(!client) 
        {
           return;
        }
        /* Lee la información enviada por el cliente. */
        consultarPeticion(client);
     }
     else if (iniciarCliente())
     {              
        Serial.print('F');
        tomarImagen(client);
        /* Este delay es necesario ya que este es el estado donde se toma la foto diaria.
         * Debe ser bloqueante debido a la necesidad de que el SE quede en estado FOLLAJE
         * para que la camara tome correctamente la imagen. Que el SE este con el boton
         * prendido no genera un conflicto al tomar la imagen.
         */
        delay(2000);
        /* Una vez tomada la foto, vuelve al ultimo estado en el que se encontraba */
        Serial.print(lastState);
     }
     else if(currentMillis - startMillis < tiempoMaxParaFoto)
     {
        Serial.println("Error al sacar foto.");
     }
     else
     {
      /* Si se excede tiempoMaxParaFoto y aun no se consiguio una respuesta
       * del servidor, se produce un timeout y deja de realizar peticiones.
       */
        startMillis = millis();
     }
  }
}
