#include <stdio.h>

int main(){
    char vetor[3];
    for (int a = 0; a < 3; a++){
        printf("%d\n", a);
        scanf("%c", &vetor[a]);
    }
}
