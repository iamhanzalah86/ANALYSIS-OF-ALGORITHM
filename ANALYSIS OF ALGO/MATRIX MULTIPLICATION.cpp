#include <iostream>
using namespace std;

const int N = 3;

void matrixMultiplication(int A[][N], int B[][N], int C[][N], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0;
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void printMatrix(int mat[][N], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << mat[i][j] << " ";
        }
        cout << endl;
    }
}

int main() {
    int A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int B[N][N] = {{10, 11, 12}, {13, 14, 15}, {16, 17, 18}};
    int C[N][N] = {0};
    matrixMultiplication(A, B, C, N);
    cout << "Resultant matrix:\n";
    printMatrix(C, N);
    return 0;
}
