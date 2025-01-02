#include "HC_SR04.h"
#define HCSR04_TIMEOUT 1000000

void ultrasonic_init() {
    Gpio_initPin(&DDRD, OUTPUT, TRIG_PIN_1);
    Gpio_initPin(&DDRD, INPUT, ECHO_PIN_1);
    Gpio_initPin(&DDRB, OUTPUT, TRIG_PIN_2);
    Gpio_initPin(&DDRB, INPUT, ECHO_PIN_2);
    Gpio_initPin(&DDRB, OUTPUT, TRIG_PIN_3);
    Gpio_initPin(&DDRB, INPUT, ECHO_PIN_3);
}

// void trigger_pulse() {
//     PORTD &= ~(1 << TRIG_PIN);
//     _delay_us(2);
//     PORTD |= (1 << TRIG_PIN);
//     _delay_us(10);
//     PORTD &= ~(1 << TRIG_PIN);
// }

// uint16_t measure_distance() {
//     uint16_t count = 0;
//     trigger_pulse();

//     // Echo 신호가 HIGH로 전환될 때까지 대기
//     while (!(PIND & (1 << ECHO_PIN)));

//     // Echo 신호가 LOW로 전환될 때까지 타이머 시작
//     TCNT0 = 0;  // Timer 초기화
//     while (PIND & (1 << ECHO_PIN)) {
//         if (TCNT0 >= 255) {
//             count++;
//             TCNT0 = 0;
//         }
//     }

//     // 총 시간을 계산 (타이머 오버플로우 수와 타이머 값 사용)
//     uint16_t timer_count = (count * 256) + TCNT0;

//     // 거리 계산 (음속 340m/s 사용)
//     uint16_t distance = (timer_count * 64.0 * 1000000.0) / (F_CPU / 2) / 58;

//     return distance;
// }

uint32_t measure_distance1(){
    uint32_t time = 0;
    uint32_t timeout = HCSR04_TIMEOUT;

    PORTD &= ~(1 << TRIG_PIN_1);
    _delay_us(2);
    PORTD |= (1 << TRIG_PIN_1);
    _delay_us(10);
    PORTD &= ~(1 << TRIG_PIN_1);

    while (!(PIND & (1 << ECHO_PIN_1))){
        if(timeout-- == 0) return -1;
    }
    while (PIND & (1 << ECHO_PIN_1)){
        if(time++ >= 5000) break;
        _delay_us(1);
    }

    uint32_t distance = time / 58;

    return distance;
}

uint32_t measure_distance2(){
    uint32_t time = 0;
    uint32_t timeout = HCSR04_TIMEOUT;

    PORTB &= ~(1 << TRIG_PIN_2);
    _delay_us(2);
    PORTB |= (1 << TRIG_PIN_2);
    _delay_us(10);
    PORTB &= ~(1 << TRIG_PIN_2);

    while (!(PINB & (1 << ECHO_PIN_2))){
        if(timeout-- == 0) return -1;
    }
    while (PINB & (1 << ECHO_PIN_2)){
        if(time++ >= 5000) break;
        _delay_us(1);
    }

    uint32_t distance = time / 58;

    return distance;
}

uint32_t measure_distance3(){
    uint32_t time = 0;
    uint32_t timeout = HCSR04_TIMEOUT;

    PORTB &= ~(1 << TRIG_PIN_3);
    _delay_us(2);
    PORTB |= (1 << TRIG_PIN_3);
    _delay_us(10);
    PORTB &= ~(1 << TRIG_PIN_3);

    while (!(PINB & (1 << ECHO_PIN_3))){
        if(timeout-- == 0) return -1;
    }
    while (PINB & (1 << ECHO_PIN_3)){
        if(time++ >= 5000) break;
        _delay_us(1);
    }

    uint32_t distance = time / 58;

    return distance;
}