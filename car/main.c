#include "AP/apMain.h"

int main(void) {
    apMain_init();
    while (1) {
        apMain_execute();
    }
    return 0;
}
