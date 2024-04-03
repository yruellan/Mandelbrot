# Mandelbrot and Julia sets

## How to use

This simulation uses Processing. You can download the Processing application [here](https://processing.org/download) to run my simulation.

Keyboard actions :
- Arrows : move view
- `:` and `=` : zoom or dezoom
- `l` and `m` : progressive zoom
- `o` and `p` : increase or decrease number of itterations
- `;` : change display mode (Mandelbrot, Julia or JuliaSDF)
- `alt` : reset scene

## Simulation

This project use a GLSL shader to calculate the Mandelbrot or the Julia set.

### Mandelbrot Set

We define $c$ a complex number for each pixel, depending of zoom and position of camera. We define the sequence $z_0 = 0$ and $z_{n+1}=z^2+c$. The color represents the number of iterations needed to diverge (ie $\lvert{z_n}\rvert>2$). 

<img src="image/img1.png" width="350">


### Julia Set

The Julia set is similar to the Mandelbrot set, but now $z_0$ is the position on the screen and $c$ is predetermined.

<img src="image/img2.png" width="350">

### Julia Set by SDF

An SDF is a signed distance function. This algorithm tries to calculate the distance to the Julia set. 

To compute this distance, we compute the $z_n$ sequence, and at same time its derivative. So we get $dz_{n+1} = 2 * z * dz $. With this derivative, we can calulate something called the Hubbard-Douady potential $ G_c(z_0) $. We can use this potential to approximate the distance $d_c = \frac{G_c(z_0)}{\nabla G_c(z_0)}$. In our case, we get $d_c =  \lvert{z_n}\rvert  \frac{\log{\lvert{z_n}\rvert}}{ \lvert{dz_n}\rvert} $. You can find more explanations [here](https://iquilezles.org/articles/distancefractals/).

## Some Pictures

<img src="image/img6.png" width="350">
<img src="image/img3.png" width="350">
<img src="image/img4.png" width="350">
<img src="image/img5.png" width="350">
<img src="image/img7.png" width="350">
