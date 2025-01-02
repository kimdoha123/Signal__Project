#ifndef APMAIN_H_
#define APMAIN_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "../Periph/TIM/TIM.h"
#include "../Periph/UART0/UART0.h"
#include "Service/Service.h"
void apMain_init();
void apMain_execute();
#endif