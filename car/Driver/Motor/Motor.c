#include "Motor.h"


void Motor_init(){
	Gpio_initPin(&DDRB, OUTPUT, MOTOR_PWM);
	Gpio_initPin(&DDRB, OUTPUT, MOTOR1_IN1);
	Gpio_initPin(&DDRB, OUTPUT, MOTOR1_IN2);
	Gpio_initPin(&DDRB, OUTPUT, MOTOR2_IN3);
	Gpio_initPin(&DDRB, OUTPUT, MOTOR2_IN4);
}

void Motor_speedMode(uint16_t data){
	MOTOR_ICR = (250000 / 250) - 1;
	if(data == 0) MOTOR_OCR = 0;
	else MOTOR_OCR = MOTOR_ICR / data;
}
void Motor_Control(uint8_t action) {
    switch (action) {
        case 0:
			Gpio_writePin(&PORTB, MOTOR1_IN1, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR1_IN2, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR2_IN3, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR2_IN4, GPIO_PIN_RESET);
            break;
        case 2:
			Gpio_writePin(&PORTB, MOTOR1_IN1, GPIO_PIN_SET);
            Gpio_writePin(&PORTB, MOTOR1_IN2, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR2_IN3, GPIO_PIN_SET);
            Gpio_writePin(&PORTB, MOTOR2_IN4, GPIO_PIN_RESET);
            break;
        case 4:
            Gpio_writePin(&PORTB, MOTOR1_IN1, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR1_IN2, GPIO_PIN_SET);
            Gpio_writePin(&PORTB, MOTOR2_IN3, GPIO_PIN_SET);
            Gpio_writePin(&PORTB, MOTOR2_IN4, GPIO_PIN_RESET);
            break;

        case 5:
            Gpio_writePin(&PORTB, MOTOR1_IN1, GPIO_PIN_SET);
            Gpio_writePin(&PORTB, MOTOR1_IN2, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR2_IN3, GPIO_PIN_RESET);
            Gpio_writePin(&PORTB, MOTOR2_IN4, GPIO_PIN_SET);
            break;
    }
}
