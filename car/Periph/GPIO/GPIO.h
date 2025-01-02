#ifndef GPIO_H_
#define GPIO_H_
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>

enum {OUTPUT, INPUT};
enum {GPIO_PIN_RESET, GPIO_PIN_SET};
void Gpio_initPort(volatile uint8_t* DDR, uint8_t dir);
void Gpio_initPin(volatile uint8_t* DDR, uint8_t dir, uint8_t pinNum);
void Gpio_writePort(volatile uint8_t* PORT, uint8_t data);
void Gpio_writePin(volatile uint8_t* PORT, uint8_t pinNum, uint8_t state);
uint8_t Gpio_readPort(volatile uint8_t* PIN);
uint8_t Gpio_readPin(volatile uint8_t* PIN, uint8_t pinNum);

#endif