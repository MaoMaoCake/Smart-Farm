#include <IRremote.h>

const uint16_t recvPin = 23; //26 D4, ПИН подсоединения ИК приемника  
const uint16_t kCaptureBufferSize = 1024;
decode_results result;
IRrecv ir(recvPin, kCaptureBufferSize);

void setup() {
   Serial.begin(115200);
   Serial.println("Starting IR-receiver...");
   ir.enableIRIn();
   Serial.println("IR-receiver active");
   //digitalWrite(sendPin, HIGH);
  
 }

void loop() {
     if (ir.decode(&result)) {
     Serial.println(result.value, HEX);
     Serial.println(result.value);
     switch (result.decode_type){
      case NEC: Serial.println("NEC"); break ;
      case SONY: Serial.println("SONY"); break ;
      case RC5: Serial.println("RC5"); break ;
      case RC6: Serial.println("RC6"); break ;
      case SHARP: Serial.println("SHARP"); break ;
      case SAMSUNG: Serial.println("SAMSUNG"); break ;
      default:
        case UNKNOWN: Serial.println("UNKNOWN"); break ;
      }
     ir.resume();
   }
}
