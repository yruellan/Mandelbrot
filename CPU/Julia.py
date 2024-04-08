from PIL import Image
from ctypes import cdll,POINTER,c_float,c_int,CDLL
from tqdm import tqdm
from time import time
from enum import Enum, auto

class Mode(Enum):
    """Image simulation mode"""
    PYTHON = auto()
    C = auto()
    C_COLOR = auto()

class Preview(Enum):
    """Image preview mode"""
    Show = auto()
    Autosave = auto()
    


def timeit(f):
    """A decorator to time a function"""
    def warpper(*args,**kwargs):
        t0 = time()
        r = f(*args,**kwargs)
        t1 = time()
        print(f"Execute {f.__name__}{args,kwargs} in {t1-t0:10.3f}s")
        return r
    return warpper


def import_c_lib():
    """Load library.so
        You need first to compile library.cpp with
        `g++ -c -fPIC test.cpp -o test.o` and 
        `g++ -shared -o test.so test.o`
        to use this function.
    """

    try: myCppModule = cdll.LoadLibrary('./library.so')
    except OSError: myCppModule = cdll.LoadLibrary('CPU/library.so')

    myCppModule.Julia.argtypes = [c_float,c_float,c_float,c_float,c_int]
    myCppModule.Julia.restype = c_float
    myCppModule.JuliaColor.argtypes = [c_float,c_float,c_float,c_float,c_int]
    myCppModule.JuliaColor.restype = POINTER(c_int)
    return myCppModule

def Hue2RGB(h:float)->list[int]:
    """Convert a hue to RGB color"""
    
    col = [0,0,0]

    if (h==-1): return tuple(col) 

    if (h == 1.0): h = 0.0 
    i = int(h*6.0)
    f = int(255*(h*6.0 - i))
    
    if (i==0): col[0] = 255 ; col[1] = f ; col[2] = 0 ; 
    if (i==1): col[0] = 255-f ; col[1] = 255 ; col[2] = 0 ; 
    if (i==2): col[0] = 0 ; col[1] = 255 ; col[2] = f ; 
    if (i==3): col[0] = 0 ; col[1] = 255-f ; col[2] = 255 ; 
    if (i==4): col[0] = f ; col[1] = 0 ; col[2] = 255 ; 
    if (i==5): col[0] = 255 ; col[1] = 0 ; col[2] = 255-f ;

    return tuple(col)

def Julia(z_x,z_y,c_x,c_y,itt) -> float :
    """Calculate the Julia fractal for c = (`c_x`,`c_y`)
        at the point z_0 = (`z_x`,`z_y`) with `itt` iteration 
    """
    for i in range(itt):
        # z = z**2 + c

        temp = 2.0*z_x*z_y + c_x
        z_x = z_x*z_x - z_y*z_y + c_y
        z_y = temp

        if z_x**2+z_y**2 > 2 : return float(i)/itt
    return -1.0


@timeit
def image(
        size=700,
        itt=1000,
        mode : Mode = Mode.PYTHON,
        julia_c : None | tuple[float] | complex = None,
        preview : Preview | str = Preview.Show,
    ):

    if not isinstance(mode, Mode):
        raise TypeError(f"mode should be an Mode object and not an {type(mode)}")
    if not isinstance(preview, Preview) and not isinstance(preview, str):
        raise TypeError(f"preview should be an Preview object or an str, not an {type(preview)}")

    img = Image.new('RGB', (size,size))
    pixel = img.load()
    is_debuging = False
    
    myCppModule : CDLL | None
    if Mode is Mode.PYTHON:
        myCppModule = None
    else :
        myCppModule = import_c_lib()
    
    if is_debuging:
        x,y,c_x,c_y,itt = 0,0,0,0,100
        print(f"{Julia(x,y,c_x,c_y,itt)=}")
        print(f"{myCppModule.Julia(x,y,c_x,c_y,itt)=}")
        myCppModule.JuliaColor.restype = c_int*3
        print(f"{myCppModule.JuliaColor(x,y,c_x,c_y,itt)=}") 
        print(f"{myCppModule.JuliaColor(x,y,c_x,c_y,itt)[:3]=}") 
        return

    for ij in tqdm(range(size**2)):
        i = ij // size
        j = ij % size 
        x = 2 * float(i) / size - 1
        y = 2 * float(j) / size - 1
        # x *= 1.5
        # y *= 1.5

        args: tuple[float, float, float, float, int]
        if julia_c is None :
            args = (0,0,x,y,itt)
        elif isinstance(julia_c, complex):
            args = (x,y,julia_c.real,julia_c.imag,itt)
        else :
            args = (x,y,julia_c[0],julia_c[1],itt)

        if mode == Mode.PYTHON or mode == Mode.C:
            if mode == Mode.PYTHON: k =  Julia(*args)
            else : k = myCppModule.Julia(*args)

            if k == -1.0 : 
                pixel[i,j] = (0,0,0)
                break
            HUE = k * 10.0

            # RGB = hsv2rgb(HUE,1.0,1.0)
            # col = tuple(int(255*x) for x in RGB)
            col = Hue2RGB(HUE)
        elif mode == Mode.C_COLOR:
            t = myCppModule.JuliaColor(*args)
            col = (t[0], t[1], t[2])
        
        # switch between math and computer coordonate
        pixel[j,i] = col 

    if preview is Preview.Show :
        img.show()
    elif preview is Preview.Autosave :
        img.save(f'Julia_img/Fractal({c_x},{c_y} ; {size}).png')
    else :
        file_source : str = preview[1]
        img.save(file_source)

if __name__ == "__main__":
    
    julia_c = -0.15, -0.78 

    image(
        size = 700,
        itt = 1000,
        mode = Mode.C_COLOR,
        julia_c = julia_c, # or None to get the Mandelbrot set
        preview = Preview.Show # or Preview.Autosave or Preview.Save("location.jpg")
    )