#ifndef LISTENER_H_
#define LISTENRE_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include "../../Driver/Motor/Motor.h"
#include "../../Periph/UART0/UART0.h"
#include "../../Driver/HC_SR04/HC_SR04.h"
#include "../../Model/Model_MotorDirectionState/Model_MotorDirectionState.h"
#include "../../Model/Model_MotorUARTState/Model_MotorUARTState.h"
#include "../../Model/Model_MotorHCState/Model_MotorHCState.h"

enum {STOP = 0, GO = 2, LEFT = 4, RIGHT = 5, SLOW = 6};

void Listener_init();
void Listener_EventCheck();
void Listener_MotorHCEvent();
void Listener_MotorUartEvent();
void Listener_MotorDirectionEvent();
#endif