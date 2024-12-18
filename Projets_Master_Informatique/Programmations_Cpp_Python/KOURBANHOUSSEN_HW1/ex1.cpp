#include <iostream>


int main(){
    int size_tree; 
    std::cin>>size_tree; // taille du sapin

    if (size_tree<=2){ // si la taille du sapin est inferieur ou egale a 2 
        std::cerr<<"Tree is too small."<<std::endl;
    }else{
        for(int i=0; i<size_tree; ++i){
            for(int x=0; x<size_tree-i-1; ++x){
                std::cout<<" ";
            }
            for(int y=0; y<i+1; ++y){
                std::cout<<"*";
            }
            for(int z=0; z<i; ++z){
                std::cout<<"*";
            }
            std::cout<<""<<std::endl;
        }
        for(int j=0; j<size_tree-2; ++j){
            std::cout<<" ";
        }
        std::cout<<"| |"<<std::endl;
    }
    return 0;
}