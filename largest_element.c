#include <stdio.h>

// Function to find the largest element in a matrix
int findLargest(int mat[][100], int m, int n) {
    int largest = mat[0][0]; // Initialize largest element to the first element in the matrix
    int i, j;
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            if (mat[i][j] > largest) {
                largest = mat[i][j];
            }
        }
    }
    return largest;
}

int main() {
    int mat[3][3] = {{1, 2, 3},
                     {4, 5, 6},
                     {7, 8, 9}};
    int m = 3, n = 3;
    int largest = findLargest(mat, m, n);
    printf("The largest element in the matrix is: %d\n", largest);
    return 0;
}