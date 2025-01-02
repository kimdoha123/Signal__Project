#include "GPIO.h"

//GPIO 기능 ?

//DDR 1.Port 2. pin

void Gpio_initPort(volatile uint8_t* DDR, uint8_t dir){
	//DDR
	//ex) DDRD = 0xff; (한번에 하는거)
	//Mode : Input, Output
	if(dir == OUTPUT){
		*DDR = 0xff;
	}
	else{
		*DDR = 0x00;
	}
}

void Gpio_initPin(volatile uint8_t* DDR, uint8_t dir, uint8_t pinNum){
	//DDR
	//ex) DDRD |= (1<<0) | (1<<1);
	if(dir == OUTPUT){
		*DDR |= (1<<pinNum);
	}
	else{
		*DDR &= ~(1<<pinNum);
	}
}

void Gpio_writePort(volatile uint8_t* PORT, uint8_t data){
	*PORT = data;
}

void Gpio_writePin(volatile uint8_t* PORT, uint8_t pinNum, uint8_t state){
	if(state == GPIO_PIN_SET){
		*PORT |= (1<<pinNum);
	}
	else{
		*PORT &= ~(1<<pinNum);
	}
}

uint8_t Gpio_readPort(volatile uint8_t* PIN){
	//무슨 변수 = PINA
	return *PIN;
}

uint8_t Gpio_readPin(volatile uint8_t* PIN, uint8_t pinNum){
	// PINA & (1<<0);
	// 풀업저항 기준, 입력 받으면 0이기에 눌려졌을 때 0이 리턴되어야 함
	return ((*PIN & (1<<pinNum)) != 0);		//눌리면(0) 해당값이 거짓이므로 0리턴
}