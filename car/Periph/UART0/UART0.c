#include "UART0.h"

uint8_t uart0Rxbuff[100];
uint8_t uart0RxFlag;

void USART_init(void){
    UBRR0H = 0x00;            // 9600bps로 설정
    UBRR0L = 207;             
    UCSR0A |= (1<<U2X0);      // 2배속 모드 활성화
    UCSR0C |= (1<<UCSZ01) | (1<<UCSZ00);  // 8비트 데이터
    UCSR0B |= (1<<RXEN0) | (1<<TXEN0);    // 송수신 활성화
    UCSR0B |= (1<<RXCIE0);    // 수신 인터럽트 활성화
}

void UART0_ISR_Process(){
	static uint8_t uart0RxTail = 0;
	uint8_t rx0Data = UDR0;
	if(rx0Data == '\n'){
		uart0Rxbuff[uart0RxTail] = rx0Data;
		uart0RxTail++;
		uart0Rxbuff[uart0RxTail] = 0;
		uart0RxTail = 0;
		uart0RxFlag = 1;
		}else{
		uart0Rxbuff[uart0RxTail] = rx0Data;
		uart0RxTail++;
	}
}

void USART_Transmit(unsigned char data)
{
    while (!(UCSR0A & (1<<UDRE0)));
    UDR0 = data;
}



unsigned char USART_Receive(void)
{
    while (!(UCSR0A & (1<<RXC0)));
    return UDR0;
}

void UART0_sendString(char *str){
	for(int i = 0; str[i]; i++){
		USART_Transmit(str[i]);
	}
}

void UART0_clearRxFlag(){
	uart0RxFlag = 0;
}

void UART0_setRxFlag(){
	uart0RxFlag = 1;
}

uint8_t UART0_getRxFlag(){
	return uart0RxFlag;
}


uint8_t* UART0_readRxBuff(){
	return uart0Rxbuff;
}