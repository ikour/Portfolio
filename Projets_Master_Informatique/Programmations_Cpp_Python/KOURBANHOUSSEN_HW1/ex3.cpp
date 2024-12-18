#include <iostream>
#include <vector>

int main(){

    int n; // taille du vecteur
    std::cin>>n; 

    std::vector <int> vector_1(n); // vecteur 1 de taille n
    std::vector <int> vector_2(n); // vecteur 2 de taille n
    std::vector <int> vector_res(n); // vecteur res, multiplication des vecteurs 1 et 2

    for (std::vector<int>::iterator it = vector_1.begin(); it != vector_1.end(); it++){
        std::cin >> *it;
    }
    for (std::vector<int>::iterator it = vector_2.begin(); it != vector_2.end(); it++){
        std::cin >> *it;
    }

    std::vector<int>::iterator it_1 = vector_1.begin();
    std::vector<int>::iterator it_2 = vector_2.begin();
    std::vector<int>::iterator it_res = vector_res.begin();
    while(it_1!=vector_1.end()){
        *it_res = *it_1 * *it_2;
        ++it_1; ++it_2; ++it_res;
    }
    int i = 0;
    for (std::vector<int>::iterator it = vector_res.begin(); it != vector_res.end(); it++){
        if(i>=1){
            std::cout<<" ";
        }
        std::cout<<*it;
        i++;
    }

    std::cout<<""<<std::endl;

    return 0;
}
