#ifndef MODEL_MOTORUARTSTATE_H_
#define MODEL_MOTORUARTSTATE_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>


uint8_t Model_getMotorUARTStateData();
void Model_setMotorUARTStateData(uint8_t state);
#endif