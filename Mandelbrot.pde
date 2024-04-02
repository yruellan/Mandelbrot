PShader shader;
PVector center ;
float zoom ;
float dzoom ;
boolean reload ;
int NB_ITER ;
int draw_type ;

void setup(){
  
  size(800,800,P2D);
  
  zoom = 1 ;
  dzoom = 0 ;
  reload = true ;
  center = new PVector(0,0);
  set_shader("shader.glsl") ;
  NB_ITER = 50 ;
  draw_type = 0 ;
  
  //frameRate(30);
  
}

void set_shader(String file){
  shader = loadShader(file);
  //shader.set("u_mouse", width*.75+float(mouseX),height/2-mouseY);
  shader.set("zoom", zoom);
  shader.set("NB_ITER", NB_ITER);
  shader.set("center",center.x,center.y);
  shader(shader);
}

void draw(){
  if (dzoom != 0){
    zoom *= 1 + dzoom ;
    shader.set("zoom", zoom);
    rect(0,0,width,height);
  } else if (reload) rect(0,0,width,height);
  
  reload = false ;
}

void keyPressed(){
  
  float dz = 1.3 ;
  float dx = zoom * 30.0 ;
  
  if      (key == '=') zoom /= dz ;
  else if (key == ':') zoom *= dz ;
  else if (key == ' ') {
    set_shader("shader.glsl");
    
  }
  else if (keyCode == 37)  center.x += dx ;
  else if (keyCode == 38)  center.y -= dx ;
  else if (keyCode == 39)  center.x -= dx ;
  else if (keyCode == 40)  center.y += dx ;
  else if (keyCode == 18)  zoom = 1 ; // alt
  else if (key == 'm')  dzoom -= 0.01 ;
  else if (key == 'l')  dzoom += 0.01 ;
  else if (key == 'o')  NB_ITER -= 50 ;
  else if (key == 'p')  NB_ITER = min(50,NB_ITER-50) ;
  else if (key == ';')  draw_type = (draw_type+1)%3 ;
  else println(key,keyCode);
  
  shader.set("zoom", zoom);
  shader.set("center",center.x,center.y);
  shader.set("NB_ITER", NB_ITER);
  shader.set("draw_type", draw_type);
  reload = true ;
}

void mouseMoved(){
  //shader.set("u_mouse", float(mouseX),height-float(mouseY));
}
