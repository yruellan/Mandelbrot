#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform vec2 center;
uniform vec2 resolution;

uniform float zoom;
uniform int NB_ITER;
uniform int draw_type;
uniform vec2 julia_c ; 
// #define julia_c vec2(-0.545,0.6)

float julia(vec2 z0, vec2 c){

    dvec2 z = dvec2(z0) ;
    dvec2 c_ = dvec2(c) ;

    for (int i = 0 ; i < NB_ITER ; i++){

        z = dvec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c_ ; // z = z^2 + c

        // if (dot(z,z)>4.0) return float(i)/float(NB_ITER) ;
        if (dot(z,z)>4.0) return float(i) ;
    }
    return -1.0 ;
}

float mandelbrot(vec2 pos){
    return julia(vec2(0.0,0.0),pos) ;
}

float juliaSDF(vec2 z0, vec2 c){
    vec2 z = z0 ;
    vec2 dz = vec2(1,0) ;

    for (int i = 0 ; i < NB_ITER ; i++){

        dz = 2.0 * vec2(dz.x*z.x - dz.y*z.y, dz.x*z.y + dz.y*z.x);
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c ;

    }
    float norm_z = sqrt(dot(z,z)) ;
    float norm_dz = sqrt(dot(dz,dz)) ;

    // Distance apporximation with Hubbard-Douady potential
    return norm_z * log(norm_z) / norm_dz ;
}



vec3 hsl2rgb( in vec3 c ){
    // Convert color from HSL to RGB
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

    return c.z + c.y * (rgb-0.5)*(1.0-abs(2.0*c.z-1.0));
}


void main() {
    vec2 pos = 2.0 * gl_FragCoord.xy / resolution ;

    // Calculate the complex number of the position
    pos -= vec2(1,1) ;
    pos *= zoom ;
    pos -= vec2(.5,0) ;
    pos -= 2.0*center/resolution ;


    
    // Calculate the color
    float i ; 
    if (draw_type == 0)      i = mandelbrot(pos) ;
    else if (draw_type == 1) i = julia(pos, julia_c) ;
    else                     i = juliaSDF(pos, julia_c) ;

    float HUE = sqrt(i)/30.0 ;
    vec3 col = hsl2rgb(vec3(HUE,1,0.5));
    
    gl_FragColor = (i==-1.0) ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(col,1.0) ;


}