#include <iostream>
using namespace std;

extern "C" float Julia(float z_x,float z_y,float c_x,float c_y,int itt = 1000){
    float temp ;
    for (float i = 0.0 ; i < itt ; i++){
        // z = z**2 + c

        temp = 2.0*z_x*z_y + c_x ;
        z_x = z_x*z_x - z_y*z_y + c_y ;
        z_y = temp ;

        if (z_x*z_x+z_y*z_y > 2) {
            return i/itt ;
        } ;
    }
    return -1.0 ;
}

extern "C" double julia(int x, int y, int X, int Y, int Max){
    double temp ;
    double za = 0 ;
    double zb = 0 ;

    double c_a = ( 3.5 * x ) / ( X - 1.0 ) - 2.5 ;
    double c_b = ( -2.5 * y ) / ( Y - 1.0 ) + 1.25 ;

    int i = 0 ;
    while ( i < Max && (za * za + zb * zb) < 4 ){
        // z = za * za - zb * zb  +  za * zb + zb * za  +  ca + cb
        temp = za * za - zb * zb + c_a ;
        zb = za * zb * 2 + c_b ;
        za = temp ;
        i++ ;
    }

    return 8*i / ((double) Max ) * 255;

}

extern "C" double* loop(int X, int Y, int Max){
    double l[X][Y] ;
    for ( int i = 0; i < X ; i++){
        for ( int j = 0; j < Y ; j++){
            l[i][j] = julia(i,j,X,Y,Max) ;
        }
    }
    double* p = new double ;
    return p ;
}

extern "C" int* point(){
    int a[2] = {2, 3} ;
    int* p = &a[2] ;
    cout << "a  = " << a << endl ;
    cout << "&a = " << &a << endl ;
    cout << "*a = " << p << endl ;
    return p ;
}

