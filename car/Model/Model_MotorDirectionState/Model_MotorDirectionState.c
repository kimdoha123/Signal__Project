#include "Model_MotorDirectionState.h"

uint8_t MotorDirectionState;

uint8_t Model_getMotorDirectionStateData(){
	return MotorDirectionState;
}

void Model_setMotorDirectionStateData(uint8_t state){
	MotorDirectionState = state;
}