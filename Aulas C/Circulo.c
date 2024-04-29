#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
bool valido;
float raio, area;
const pi = 3.1415;
int escolha, raio;

bool defarea(){
    valido = false;
    while(valido != true){
        printf("Defina o raio a ser calculado a area do circulo:\n\n");
        scanf("%d", &raio);
        if(raio < 0){
            printf("Valor invalido para se calcular a area, tente novamente\n\nDefina o raio a ser calculado a area do circulo:\n\n"); 
        }
        else{
            area = pi * raio * raio;
            prinf("A area do circulo com raio igual a %.1f é de %.2f\n", raio, area);
            valido = true;
        }
    }
    return;
}

void main(){
    do{
    printf("Escolha o que deseja fazer dentre as opções a seguir:\n 1-Area do circulo baseado em seu raio\n 2-...\n 0-Sair\n\n");
    scanf("%d", &escolha);
    if (escolha == 1){
        defarea();
        }
    } while(escolha != 0);
}
