#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
bool valido;
float raio, area, pi = 3.1415;
int escolha;

bool defarea(){
    printf("Defina o raio a ser calculado a area do circulo:\n\n");
    scanf("%f", &raio);
    if(raio < 0){
        printf("Valor invalido para se calcular a area, tente novamente\n\n"); 
    }
    else{
        area = pi * raio * raio;
        printf("A area do circulo com raio igual a %.1f equivale a %.2f\n", raio, area);
    }
    return valido;
}

int main(){
    do{
    printf("Escolha o que deseja fazer dentre as opes a seguir:\n 1-Area do circulo baseado em seu raio\n 2-...\n 0-Sair\n\n");
    scanf("%d", &escolha);
    if (escolha == 1){
        defarea();
        }
    } while(escolha != 0);
    return 0;
}
