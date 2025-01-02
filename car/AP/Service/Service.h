#ifndef SERVICE_H_
#define SERVICE_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include "../Listener/Listener.h"
#include "../../Model/Model_MotorDirectionState/Model_MotorDirectionState.h"
#include "../../Model/Model_MotorUARTState/Model_MotorUARTState.h"
#include "../../Model/Model_MotorHCState/Model_MotorHCState.h"

void Service_MotorData();
void Service_execute();
#endif