#ifndef MODEL_MOTORHCSTATE_H_
#define MODEL_MOTORHCSTATE_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>


uint8_t Model_getMotorHCStateData();
void Model_setMotorHCStateData(uint8_t state);
#endif