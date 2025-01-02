# Makefile

CC = avr-gcc
MCU_NAME = atmega328p

# F_CPU 설정 (16MHz)
F_CPU = 16000000UL

TARGET = main
PROG_TYPE = arduino
PORT_NAME = /dev/ttyACM0
BAUD = 115200

RM = rm -rf

# 소스 파일 목록 - 여러 폴더에 있는 소스 파일을 포함
SRC = main.c \
	AP/Listener/Listener.c \
	AP/Service/Service.c \
	AP/apMain.c \
	Model/Model_MotorDirectionState/Model_MotorDirectionState.c \
	Model/Model_MotorUARTState/Model_MotorUARTState.c \
	Model/Model_MotorHCState/Model_MotorHCState.c \
    Periph/GPIO/GPIO.c \
    Periph/TIM/TIM.c \
    Periph/UART0/UART0.c \
	Driver/HC_SR04/HC_SR04.c \
	Driver/Motor/Motor.c


# 오브젝트 파일 목록 (.c -> .o)
OBJ = $(SRC:.c=.o)

# 기본 목표: HEX 파일 생성
$(TARGET): $(OBJ)
	$(CC) -mmcu=$(MCU_NAME) -DF_CPU=$(F_CPU) -Os -o $(TARGET).elf $(OBJ)
	avr-objcopy -O ihex -R .eeprom $(TARGET).elf $(TARGET).hex
	avrdude -b $(BAUD) -p $(MCU_NAME) -c $(PROG_TYPE) -P $(PORT_NAME) -U flash:w:$(TARGET).hex

# 각 .o 파일 생성 규칙
%.o: %.c
	$(CC) -mmcu=$(MCU_NAME) -DF_CPU=$(F_CPU) -Os -c $< -o $@

# 청소: 생성된 .o, .elf, .hex 파일 제거
clean:
	$(RM) $(OBJ) $(TARGET).elf $(TARGET).hex
