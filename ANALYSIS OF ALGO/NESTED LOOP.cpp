#include <iostream>
using namespace std;

void nestedLoops(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << i << " " << j << endl;
        }
    }
}

int main() {
    int n = 3;
    nestedLoops(n);
    return 0;
}
