#pragma GCC optimize(2)
#include <iostream>
#include <string>
#include <iomanip>
#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "hw6.hpp"
#include "image.hpp"
using namespace std;

int main() {
    unsigned int kernel_size, sharpness;
    unsigned int kernel[7] = {3, 7, 11, 15, 19, 23, 27};

    string input_file = "stanford.jpg";
    string output_file;
    image img(input_file);

    /* Compute the sharpness of origin image */
    sharpness = img.Sharpness();
    cout << "Original image:" << setw(4) << setfill(' ') << sharpness << endl;

    /* Compute the sharpness of box blur image */
    for (unsigned int i = 0; i < 7; i++) {
        image img(input_file);
        output_file = "BoxBlur.jpg";
        kernel_size = kernel[i];
        img.BoxBlur(kernel_size);
        sharpness = img.Sharpness();
        cout << "BoxBulr(" << setw(2) << setfill(' ') << kernel_size << "):"
             << setw(7) << setfill(' ') << sharpness << endl;

        if (kernel_size >= 10)
            output_file.insert(7, to_string(kernel_size));
        else {
            output_file.insert(7, to_string(kernel_size));
            output_file.insert(7, to_string(0));
        }

        img.Save(output_file);
    }

    return 0;
}

