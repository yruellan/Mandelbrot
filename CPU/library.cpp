
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

extern "C" int* JuliaColor(float z_x,float z_y,float c_x,float c_y,int itt = 1000){
    int col[3] = {0,0,0};

    float h = Julia(z_x,z_y,c_x,c_y,itt);
    h = h * 10.0 ;
    // s = 1, v = 1

    if (h==-1) return col ;

    if (h == 1.0) h = 0.0 ;
    int i = int(h*6.0);
    int f = int(255*(h*6.0 - i));
    
    if (i==0) col[0] = 255 ; col[1] = f ; col[2] = 0 ; 
    if (i==1) col[0] = 255-f ; col[1] = 255 ; col[2] = 0 ; 
    if (i==2) col[0] = 0 ; col[1] = 255 ; col[2] = f ; 
    if (i==3) col[0] = 0 ; col[1] = 255-f ; col[2] = 255 ; 
    if (i==4) col[0] = f ; col[1] = 0 ; col[2] = 255 ; 
    if (i==5) col[0] = 255 ; col[1] = 0 ; col[2] = 255-f ;

    return col ;
}
