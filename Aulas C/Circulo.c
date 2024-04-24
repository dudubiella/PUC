#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool area(){
    printf("defina o raio a ser calculado a area do circulo:\n");
    return true;
}

void main(){
    int escolha, raio;
    bool valido = false;
    do{
    printf("escolha o que deseja fazer dentre as opções a seguir:\n1-area do circulo baseado em seu raio\n");
    scanf("%d", &escolha);
    if escolha == 1{
        valido = area();
        }
    } while(valido != true)
}
