#include "HC_SR04.h"

volatile uint8_t sensor_index = 0;   // 전역 변수 정의
volatile uint32_t distance[3] = {0,}; // 각 센서의 거리 저장

void ultrasonic_init() {
    Gpio_initPin(&DDRD, OUTPUT, TRIG_PIN_1);
    Gpio_initPin(&DDRD, INPUT, ECHO_PIN_1);
    Gpio_initPin(&DDRD, OUTPUT, TRIG_PIN_2);
    Gpio_initPin(&DDRD, INPUT, ECHO_PIN_2);
    Gpio_initPin(&DDRD, OUTPUT, TRIG_PIN_3);
    Gpio_initPin(&DDRD, INPUT, ECHO_PIN_3);
}

void trigger_pulse(uint8_t sensor) {
    // 각 센서에 따라 다른 핀 사용
    if (sensor == 0) {
        PORTD &= ~(1 << TRIG_PIN_1);
        _delay_us(2);
        PORTD |= (1 << TRIG_PIN_1);
        _delay_us(10);
        PORTD &= ~(1 << TRIG_PIN_1);
    }
    else if (sensor == 1) {
        PORTD &= ~(1 << TRIG_PIN_2);
        _delay_us(2);
        PORTD |= (1 << TRIG_PIN_2);
        _delay_us(10);
        PORTD &= ~(1 << TRIG_PIN_2);
    }
    else if (sensor == 2) {
        PORTD &= ~(1 << TRIG_PIN_3);
        _delay_us(2);
        PORTD |= (1 << TRIG_PIN_3);
        _delay_us(10);
        PORTD &= ~(1 << TRIG_PIN_3);
    }
}

uint32_t measure_distance(uint8_t sensor) {
    uint32_t time = 0;
    uint32_t timeout = HCSR04_TIMEOUT;

    trigger_pulse(sensor);

    // 에코 핀 읽기
    if (sensor == 0) {
        while (!(PIND & (1 << ECHO_PIN_1))){
            if(timeout-- == 0) return -1;
        }
        while (PIND & (1 << ECHO_PIN_1)){
            if(time++ >= 5000) break;
            _delay_us(1);
        }
    } 
    else if (sensor == 1) {
        while (!(PIND & (1 << ECHO_PIN_2))){
            if(timeout-- == 0) return -1;
        }
        while (PIND & (1 << ECHO_PIN_2)){
            if(time++ >= 5000) break;
            _delay_us(1);
        }
    } 
    else if (sensor == 2) {
        while (!(PIND & (1 << ECHO_PIN_3))){
            if(timeout-- == 0) return -1;
        }
        while (PIND & (1 << ECHO_PIN_3)){
            if(time++ >= 5000) break;
            _delay_us(1);
        }
    }

    uint32_t distance = time / 58;
    return distance;
}
