#ifndef MOTOR_H_
#define MOTOR_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include "../../Periph/GPIO/GPIO.h"

#define MOTOR_PWM  1

#define MOTOR1_IN1 2
#define MOTOR1_IN2 3
#define MOTOR2_IN3 4
#define MOTOR2_IN4 5

#define MOTOR_ICR	    ICR1
#define MOTOR_OCR		OCR1A

void Motor_init();
void Motor_speedMode(uint16_t data);
void Motor_Go();
void Motor_Left();
void Motor_Right();
void Motor_Stop();
#endif