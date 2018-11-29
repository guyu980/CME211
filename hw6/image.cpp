#include "image.hpp"
#include <iostream>
#include <string>
#include "hw6.hpp"
#include <boost/multi_array.hpp>
#include <jpeglib.h>
using namespace std;

image::image (string input_file) {
    this ->input_file = input_file;
    ReadGrayscaleJPEG(input_file, img);
    m = (unsigned int) img.size();
    n = (unsigned int) img[0].size();
}

/* Save current image data into jpg file */
void image::Save(string output_file) {
    WriteGrayscaleJPEG(output_file, img);
}

/* Implement convolution */
void image::Convolution(boost::multi_array<unsigned char, 2>& input,
                        boost::multi_array<unsigned char, 2>& output,
                        boost::multi_array<float, 2>& kernel) {
    unsigned int kernel_size, d;
    float sum;
    kernel_size = (unsigned int) kernel.size();

    if (kernel_size % 2 == 0) {
        cout << "Kernel size is not odd!" << endl;
        exit(0);
    }
    
    if (kernel_size != (unsigned int) kernel[0].size()) {
        cout << "Kernel is not square!" << endl;
        exit(0);
    }
    
    if (kernel_size < 3) {
        cout << "Kernel size is less than 3!" << endl;
        exit(0);
    }

    if (input.size() != output.size() || input[0].size() != output[0].size()) {
        cout << "Size doesn't match for input and output!" << endl;
        exit(0);
    }

    d = (unsigned int) ((kernel_size-1)/2);
    boost::multi_array<unsigned char, 2> img_extend(boost::extents[m+2*d][n+2*d]);

    /* Generate extend matrix by edge padding */
    for (unsigned int i = 0; i < m+2*d; i++) {
        for (unsigned int j = 0; j < n+2*d; j++) {
            if (i < d) {
                if (j < d)
                    img_extend[i][j] = input[0][0];
                else if (j < m+d)
                    img_extend[i][j] = input[0][j-d];
                else
                    img_extend[i][j] = input[0][n-1];
            }
            else if (i < m+d) {
                if (j < d)
                    img_extend[i][j] = input[i-d][0];
                else if (j < n+d)
                    img_extend[i][j] = input[i-d][j-d];
                else
                    img_extend[i][j] = input[i-d][n-1];
            }
            else {
                if (j < d)
                    img_extend[i][j] = input[m-1][0];
                else if (j < n+d)
                    img_extend[i][j] = input[m-1][j-d];
                else
                    img_extend[i][j] = input[m-1][n-1];
            }
        }
    }

    /* Sum up the product between kernel and matrix */
    for (unsigned int i = 0; i < m; i++) {
        for (unsigned int j = 0; j < n; j++) {
            sum = 0;
            for (unsigned int k = 0; k < kernel_size; k++)
                for (unsigned int l = 0; l < kernel_size; l++)
                    sum += kernel[k][l]*img_extend[i+k][j+l];
            if (sum < 0)
                output[i][j] = (unsigned char) 0;
            else if (sum > 255)
                output[i][j] = (unsigned char) 255;
            else
                output[i][j] = (unsigned char) sum;
        }
    }
}

/* Implement box blur */
void image::BoxBlur(unsigned int kernel_size) {
    float square;
    boost::multi_array<float, 2> kernel(boost::extents[kernel_size][kernel_size]);
    square = (float) (kernel_size * kernel_size);

    for (unsigned int i = 0; i < kernel_size; i++)
        for (unsigned int j = 0; j < kernel_size; j++)
            kernel[i][j] = 1 / square;

    image::Convolution(img, img, kernel);
}

/* Compute the sharpness of current image */
unsigned int image::Sharpness(void) {
    boost::multi_array<float, 2> kernel(boost::extents[3][3]);
    float element[3][3] = {{0, 1, 0}, {1, -4, 1}, {0, 1, 0}};
    unsigned int max = 0;

    for (unsigned int i = 0; i < 3; i++)
        for (unsigned int j = 0; j < 3; j++)
            kernel[i][j] = element[i][j];

    image::Convolution(img, img, kernel);

    for (unsigned int i = 0; i < m; i++)
        for (unsigned int j = 0; j < n; j++)
            if (img[i][j] > max)
                max = img[i][j];

    return max;
}

