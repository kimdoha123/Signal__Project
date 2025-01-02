#include "Model_MotorUARTState.h"

uint8_t MotorUARTState;

uint8_t Model_getMotorUARTStateData(){
	return MotorUARTState;
}

void Model_setMotorUARTStateData(uint8_t state){
	MotorUARTState = state;
}