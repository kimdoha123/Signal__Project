#include "Listener.h"

float distance1;  // float로 변경
float distance2;  // float로 변경
float distance3;  // float로 변경
float distance4;

void Listener_init(){
    Motor_init();
    USART_init();
    ultrasonic_init();
}

void Listener_EventCheck(){
    distance1 = distance[0];  // 첫 번째 센서의 거리 (float)
    distance2 = distance[1];  // 두 번째 센서의 거리 (float)
    distance3 = distance[2];  // 세 번째 센서의 거리 (float)
    distance4 = distance[3];
    Listener_MotorHCEvent();
    Listener_MotorUartEvent();
    Listener_MotorDirectionEvent();
}

void Listener_MotorHCEvent(){
    uint8_t MotorHCState;
    MotorHCState = Model_getMotorHCStateData();

    switch (MotorHCState){
    case STOP:
        // 하나라도 거리가 15cm 이내이면 STOP으로 전환
        if (distance1 <= 25.0 || distance2 <= 25.0 || distance3 <= 25.0 || distance4 <= 25.0) {
            Model_setMotorHCStateData(STOP);
        }
        else if ((distance1 > 25.0 && distance1 <= 30.0)
                || (distance2 > 25.0 && distance2 <= 30.0)
                || (distance3 > 25.0 && distance3 <= 30.0)
                || (distance4 > 25.0 && distance4 <= 30.0)){
            Model_setMotorHCStateData(SLOW);
        }
        else{
            Model_setMotorHCStateData(GO);
        }   
        break;
    case GO:   
        // 하나라도 거리가 15cm 이내이면 STOP으로 전환
        if (distance1 <= 25.0 || distance2 <= 25.0 || distance3 <= 25.0 || distance4 <= 25.0) {
            Model_setMotorHCStateData(STOP);
        }
        else if ((distance1 > 25.0 && distance1 <= 30.0)
                || (distance2 > 25.0 && distance2 <= 30.0)
                || (distance3 > 25.0 && distance3 <= 30.0)
                || (distance4 > 25.0 && distance4 <= 30.0)){
            Model_setMotorHCStateData(SLOW);
        }
        else{
            Model_setMotorHCStateData(GO);
        }   
        break;
    case SLOW:
        // 하나라도 거리가 15cm 이내이면 STOP으로 전환
        if (distance1 <= 25.0 || distance2 <= 25.0 || distance3 <= 25.0 || distance4 <= 25.0) {
            Model_setMotorHCStateData(STOP);
        }
        else if ((distance1 > 25.0 && distance1 <= 30.0)
                || (distance2 > 25.0 && distance2 <= 30.0)
                || (distance3 > 25.0 && distance3 <= 30.0)
                || (distance4 > 25.0 && distance4 <= 30.0)){
            Model_setMotorHCStateData(SLOW);
        }
        else{
            Model_setMotorHCStateData(GO);
        }   
        break;
    }
}

void Listener_MotorUartEvent(){
    uint8_t MotorHCState;
    MotorHCState = Model_getMotorUARTStateData();
    if(UART0_getRxFlag())
	{
		char* rxString = (char *)UART0_readRxBuff();
        if(!strcmp((uint8_t *)rxString, "STOP\n")){
            Model_setMotorUARTStateData(STOP);
            UART0_sendString("STOP\n");
        }
        else if(!strcmp((uint8_t *)rxString, "GO\n")){
            Model_setMotorUARTStateData(GO);
            UART0_sendString("GO\n");
        }
        else if(!strcmp((uint8_t *)rxString, "SLOW\n")){
            Model_setMotorUARTStateData(SLOW);
            UART0_sendString("SLOW\n");
        }
        else if(!strcmp((uint8_t *)rxString, "LEFT\n")){
            Model_setMotorUARTStateData(LEFT);
            UART0_sendString("LEFT\n");
        }
        else if(!strcmp((uint8_t *)rxString, "RIGHT\n")){
            Model_setMotorUARTStateData(RIGHT);
            UART0_sendString("RIGHT\n");
        }
        UART0_clearRxFlag();
    }
}

void Listener_MotorDirectionEvent(){
    uint8_t MotorDirectionState;
    float threshold = 0.1;  // 최소 거리 차이 기준 설정 (cm)

    MotorDirectionState = Model_getMotorDirectionStateData();

    // 임계값을 기준으로 좌우 전환
    if (((distance2 - distance3) >= threshold)) {
        Model_setMotorDirectionStateData(LEFT);
    }
    else if (((distance3 - distance2) >= threshold)) {
        Model_setMotorDirectionStateData(RIGHT);
    }
    // 거리 차이가 임계값 이하인 경우는 방향 유지
}