#include "Service.h"

static uint8_t lastMotorState = GO;  // 기본 상태를 GO로 설정

void Service_MotorData(){
    uint8_t MotorUARTState;
    uint8_t MotorHCState;
    uint8_t MotorDirectionState;

    // 상태 가져오기
    MotorUARTState = Model_getMotorUARTStateData();  // UART로부터 현재 상태 가져옴
    MotorHCState = Model_getMotorHCStateData();      // 초음파 센서로부터 현재 상태 가져옴
    MotorDirectionState = Model_getMotorDirectionStateData();

    // 1. UART 명령이 STOP이면 무조건 멈춤 상태를 유지 (SLOW 또는 GO 명령이 들어올 때까지 유지)
    if (MotorUARTState == STOP) {
        Motor_speedMode(STOP);  // 모터를 멈춤
        Motor_Control(STOP);
        UART0_sendString("Stop\n");
        lastMotorState = STOP;
        return;  // 더 이상 처리하지 않고 리턴
    }

    // 2. UART 명령이 SLOW이면 SLOW 상태를 유지 (STOP 또는 GO 명령이 들어올 때까지 유지)
    else if (MotorUARTState == SLOW) {
        Motor_speedMode(SLOW); 
        Motor_Control(GO); 
        UART0_sendString("Slow\n");
        lastMotorState = SLOW;
        return;  // 더 이상 처리하지 않고 리턴
    }

    // 3. UART 명령이 LEFT이면 왼쪽으로 회전하면서 GO 상태 유지
    else if (MotorUARTState == LEFT) {
        Motor_speedMode(GO); 
        Motor_Control(LEFT); 
        UART0_sendString("Left\n");
        lastMotorState = LEFT;
        return;
    }

    // 4. UART 명령이 RIGHT이면 오른쪽으로 회전하면서 GO 상태 유지
    else if (MotorUARTState == RIGHT) {
        Motor_speedMode(GO); 
        Motor_Control(RIGHT); 
        UART0_sendString("Right\n");
        lastMotorState = RIGHT;
        return;
    }

    // 3. UART 명령이 GO이면 기본 상태로 전환하고 초음파 상태를 확인
    else if (MotorUARTState == GO) {
        // 3-1. 초음파 상태가 STOP이면 초음파 신호에 따라 상태 변경
        if (MotorHCState == STOP) {
            Motor_speedMode(GO);    
            Motor_Control(MotorDirectionState);  // 방향에 따라 회전
            UART0_sendString("Turn\n");
            lastMotorState = STOP;  // 상태를 STOP으로 업데이트
            return;
        }
        // 3-2. 초음파 상태가 SLOW이면 속도를 줄임
        else if (MotorHCState == SLOW) {
            Motor_speedMode(SLOW); 
            Motor_Control(GO); 
            UART0_sendString("Slow\n");
            lastMotorState = SLOW;  // 상태를 SLOW로 업데이트
            return;
            
        }
        // 3-3. 기본 상태는 GO로 설정
        Motor_speedMode(GO);  // 기본 상태로 모터를 GO로 작동
        Motor_Control(GO);
        UART0_sendString("Go\n");
        lastMotorState = GO;  // 상태를 GO로 업데이트
        return;
    }
}

void Service_execute(){
    Service_MotorData();
}
