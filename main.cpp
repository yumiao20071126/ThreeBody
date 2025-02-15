// filepath: /mnt/c/Users/25367/desktop/PJ2/battle_game_2024/test_glfw.cpp
#include <iostream>
using namespace std;
int main() {
    for (int i = 0; i < 1000000000; i++) {
        i--;
        i++;
        if(i%100000000==0){
            cout<<i<<endl;
        }
    }
}