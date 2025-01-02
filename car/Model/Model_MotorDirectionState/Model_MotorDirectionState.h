#ifndef MODEL_MOTORDIRECTIONSTATE_H_
#define MODEL_MOTORDIRECTIONSTATE_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>


uint8_t Model_getMotorDirectionStateData();
void Model_setMotorDirectionStateData(uint8_t state);
#endif