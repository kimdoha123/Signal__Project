#include "TIM.h"

void TIM0_init(){
    // Timer0 설정 (Normal 모드, Prescaler 64)
    TCCR0A = 0x00;
    TCCR0B = (1 << CS01) | (1 << CS00);  // Prescaler 64
    TCNT0 = 0;  // 타이머 초기화
}

void TIM1_init(){
    TCCR1A |= ((1<<WGM11) | (0<<WGM10)); 
    TCCR1B |= ((1<<WGM13) | (1<<WGM12));
    TCCR1B |= ((0<<CS12) | (1<<CS11) | (1<<CS10));
    TCCR1A |= (1<<COM1A1) | (0<<COM1A0);
}

void TIM2_init(){
    // TIM2 타이머 설정
    TCCR2A = 0;  // CTC 모드
    TCCR2B |= (1 << WGM21);  // CTC 모드 선택
    TIMSK2 |= (1 << OCIE2A); // 타이머 인터럽트 활성화
    OCR2A = 156;             // 10ms 간격 (16MHz 클럭, 1024 프리스케일)
    TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20); // 1024 프리스케일
}

