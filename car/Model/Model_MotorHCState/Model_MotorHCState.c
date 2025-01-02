#include "Model_MotorHCState.h"

uint8_t MotorHCState;

uint8_t Model_getMotorHCStateData(){
	return MotorHCState;
}

void Model_setMotorHCStateData(uint8_t state){
	MotorHCState = state;
}