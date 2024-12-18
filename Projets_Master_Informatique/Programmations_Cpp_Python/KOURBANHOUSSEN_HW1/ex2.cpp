#include <iostream>


int main(){

    int * tab = new int [5]; // tableau des entrees

    for(int i=0; i<5; i++){
        std::cin>>tab[i];
    }

    for(int i=0; i<5; ++i){
        if(i>=1){
            std::cout<<" ";
        }

        if (tab[i] == 1){
            std::cout<<"c";
        }else if (tab[i] == 2){
            std::cout<<"c";
        }else if (tab[i] == 3){
            std::cout<<"a";
        }else if (tab[i] == 4){
            std::cout<<"d";
        }else if (tab[i] == 5){
            std::cout<<"a";
        }else if (tab[i] == 6){
            std::cout<<"a";
        }else if (tab[i] == 7){
            std::cout<<"b";
        }else if (tab[i] == 8){
            std::cout<<"b";
        }else{
            std::cout<<"b";
        }
    }
    
    delete [] tab;

    std::cout<<""<<std::endl;

    return 0;
}

