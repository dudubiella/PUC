#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
bool valido = false;
float raio, area;
const pi = 3.1415;

bool defarea(){
    printf("defina o raio a ser calculado a area do circulo:\n\n");
    scanf("%d", &raio);
    while(raio != 0){
        if(raio < 0){
            printf("Valor invalido para se calcular a area, tente novamente\n\nDefina o raio a ser calculado a area do circulo:\n\n"); 
        }
        else{
            area = pi * raio * raio;
            prinf("a area do circulo com raio igual a %.1f é de %.2f\n", raio, area);
        }
        scanf("%d", &raio);
    }
    return true;
}

void main(){
    int escolha, raio;
    
    do{
    printf("escolha o que deseja fazer dentre as opções a seguir:\n 1-area do circulo baseado em seu raio\n\n");
    scanf("%d", &escolha);
    if (escolha == 1){
        valido = defarea();
        }
    } while(valido != true);
}
main()