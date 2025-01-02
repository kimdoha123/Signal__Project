#include "apMain.h"

extern volatile uint8_t sensor_index;
extern volatile float distance[4];

ISR(USART_RX_vect){
    UART0_ISR_Process();
}

ISR(TIMER2_COMPA_vect) {
        distance[sensor_index] = measure_distance(sensor_index);  // 현재 센서의 거리 측정
        sensor_index = (sensor_index + 1) % 4;  // 다음 센서로 전환

}

void apMain_init(){
    Listener_init();
    TIM0_init();
    TIM1_init();
    TIM2_init();
    sei();
    Model_setMotorUARTStateData(GO);
    Model_setMotorUARTStateData(GO);
    Model_setMotorDirectionStateData(GO);
}

void apMain_execute(){
    Listener_EventCheck();
    Service_execute();
}
