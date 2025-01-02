#ifndef UART0_H_
#define UART0_H_
#define F_CPU 16000000UL

#define FOSC 1843200  // Clock Speed
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1

#include <avr/io.h>
#include <util/delay.h>
void UART0_ISR_Process();
void USART_init(void);
void USART_Transmit(unsigned char data);
unsigned char USART_Receive(void);
void UART0_sendString(char *str);
void UART0_clearRxFlag();
void UART0_setRxFlag();
uint8_t UART0_getRxFlag();
uint8_t* UART0_readRxBuff();
#endif