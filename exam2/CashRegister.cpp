#include "CashRegister.hpp"
#include <vector>
#include <iostream>

CashRegister::CashRegister (float change) {
    this->change = change;
}

/* Method to report changes */
void CashRegister::Print(void) {
    std::vector<int> x;
    std::vector<float> money = {20, 10, 5, 1, 0.25, 0.1, 0.05, 0.01};
    float left = change;
    
    for (int i = 0; i < 8; i++) {
        x.push_back((int) (change / money[i]));
        left -= x[i];
        std::cout << money[i] << " : " << x[i] << std::endl;
    }
}
