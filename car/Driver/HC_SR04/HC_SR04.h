#ifndef HC_SR04_H_
#define HC_SR04_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include "../../Periph/GPIO/GPIO.h"
#define HCSR04_TIMEOUT 1000000
#define TRIG_PIN_1 2
#define ECHO_PIN_1 3
#define TRIG_PIN_2 4
#define ECHO_PIN_2 5
#define TRIG_PIN_3 6
#define ECHO_PIN_3 7
#define TRIG_PIN_4 0
#define ECHO_PIN_4 1

extern volatile uint8_t sensor_index;  // 현재 측정 중인 센서 인덱스
extern volatile float distance[4];      // 각 센서의 거리 저장

void ultrasonic_init();
void trigger_pulse(uint8_t sensor);
float measure_distance(uint8_t sensor);
#endif