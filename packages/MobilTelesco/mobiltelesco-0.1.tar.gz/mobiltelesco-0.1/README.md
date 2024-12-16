
# Astrophotography Image Processing Library

This is the first-ever astrophotography image processing library that provides powerful tools for pixel-based, kernel-based, and histogram-based operations, specifically tailored to astrophotography image enhancement. The library includes operations like exposure and contrast control, clarity enhancement, noise removal, and more.

## I. Pixel-based Operations

### 1. Exposure and Contrast Control:

#### i. Linear Transformation for Contrast and Brightness:
The linear transformation formula adjusts the contrast and brightness of the image:
```
I(i,j,k) = α × I(i,j,k) + β
```
where α adjusts the contrast, and β shifts the brightness, k = r,g,b matrix.

#### ii. Exposure Adjustment:
Exposure adjustment simulates increasing or decreasing the exposure by a number of stops using the formula:
```
new_image = image × scale
```
where scale = 2^stops.
For example:
- Stops = 1 increases the exposure (brightness) by a factor of 2.
- Stops = -1 decreases the exposure (darkens the image) by a factor of 2.

#### iii. Contrast Adjustment:
The contrast is adjusted using the following formula:
```
img_contrast(x) = 1 / (1 + e^(-strength * (x - 0.5)))
```
Here:
- `x` represents the pixel intensity at position (i,j,k), and `0.5` is the reference intensity.
- `strength` controls how much contrast is applied.

The final image is:
```
adjusted_img = image_exp × image_contrast
```

### 2. Highlights and Shadow Control:
The highlights and shadows are controlled using a linear transformation in greyscale:
```
I_new(x,y) = α × I(x,y) + β
```
Where:
- α is the scaling factor (contrast).
- β is the offset (brightness).

### 3. White and Black Control (Drago’s Tone Mapping):

#### i. Luminance Calculation:
Luminance is calculated using a weighted sum of the RGB channels:
```
L(x,y) = 0.2126 × R(x,y) + 0.7152 × G(x,y) + 0.0722 × B(x,y)
```

#### ii. Logarithmic Compression:
The luminance is compressed using the natural logarithm to improve detail in darker regions:
```
L(x',y') = log(L(x,y) + 1)
```
The luminance is then normalized to the range [0,1].

#### iii. Gaussian Blur for Local Contrast:
A Gaussian blur is applied to the compressed luminance:
```
I_G(x,y) = (1 / 2πσ^2) * exp(- (x - x')^2 / 2σ^2) * L(x',y')
```

#### iv. Gamma Correction:
Gamma correction adjusts the image’s brightness and contrast:
```
img_tonemapped = image × I_G(x,y)^γ × scale
```
Where `γ` controls the brightness, and values < 1 darken the image while values > 1 brighten it.

## II. Kernel-based Operations

### 1. Texture Enhancement (Sharpening):
Sharpening is achieved through convolution with a kernel `K`:
```
Sharpened Image = Original Image + (Original Image * K) × strength
```
Where `γ` determines the level of sharpness.

### 2. Clarity Enhancement / Edge Contrast:
Edge enhancement involves Laplacian operator for edge detection and amplification:
```
Edges = ∇²f(x,y)
```
The Laplacian operator is:
```
∇²f(x,y) = ∂²f(x,y) / ∂x² + ∂²f(x,y) / ∂y²
```
Amplified edges:
```
E_amp = Edges × edge_strength
```

Blending:
```
Clarity = (I × (I - blend_factor)) + (E_amp × blend_factor)
```

## III. Histogram-based Operations

### 1. Noise Removal:

#### i. Convert to YCrCb:
The image is converted to the YCrCb color space:
```
Y = 0.2126 × B + 0.7152 × G + 0.0722 × R
```

#### ii. 2D FFT on Y Channel:
The Fast Fourier Transform (FFT) is applied to the Y channel:
```
F(u,v) = Σ Σ f(x,y) × exp(-2πi(ux/M + vy/N))
```

#### iii. Low-Pass Filter:
A low-pass filter mask is applied:
```
dist(u,v) = (u - u₀)² + (v - v₀)²
```

Blended FFT:
```
F_blended(u,v) = F_shifted(u,v) × mask(u,v) + F_shifted(u,v) × (1 - mask(u,v))
```

#### iv. Inverse FFT:
The Inverse FFT is applied to obtain the denoised image:
```
x,y = (1 / (M * N)) Σ Σ F_blended(u,v) × exp(2πi(ux/M + vy/N))
```

## Conclusion
This library provides a comprehensive set of tools for processing astrophotography images, allowing users to enhance details, control exposure, adjust contrast, and remove noise effectively. These features are especially useful for astrophotography, where fine details in dark and light regions need precise control.

