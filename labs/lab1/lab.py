#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, y, x):
        """
        Returns the value of the pixel at location (x,y).
        If the pixel value is out of range, returns the value at the nearest
        valid pixel.
        """
        y = max(0, min(self.height-1, y))
        x = max(0, min(self.width-1, x))
        return self.pixels[self.width*y + x]

    def set_pixel(self, y, x, c):
        self.pixels[y * self.width + x] = c

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height)
        for y in range(result.height):
            for x in range(result.width):
                color = self.get_pixel(y, x)
                newcolor = func(color)
                result.set_pixel(y, x, newcolor)
        return result

    def inverted(self):
        return self.apply_per_pixel(lambda c: 255-c)


    def cross_correlate(self, y, x, kernel):
        result = []
        start_y = int(y - (kernel.height - 1) / 2)
        start_x = int(x - (kernel.width - 1) / 2)
        kernel_y = 0
        for j in range(start_y, start_y + kernel.height):
            kernel_x = 0
            for i in range(start_x, start_x + kernel.width):
                result.append(self.get_pixel(j, i) * kernel.get_pixel(kernel_y, kernel_x))
                kernel_x += 1
            kernel_y += 1
        return sum(result)

    def filter_with_kernel(self, k):
        result = Image.new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                color = self.cross_correlate(y, x, k)
                result.set_pixel(y, x, color)
        return result

    def filtered(self, k):
        result = self.filter_with_kernel(k)
        result.finalize()
        return result

    def blurred(self, n):
        kernel = Image.new(n, n)
        for y in range(kernel.height):
            for x in range(kernel.width):
                kernel.set_pixel(y, x, 1/ (kernel.width * kernel.height))
        #print(kernel)
        result = self.filter_with_kernel(kernel)
        result.finalize()
        return result

    def sharpened(self, n):
        kernel = Image.new(n, n)
        for y in range(kernel.width):
            for x in range(kernel.height):
                if y == int(kernel.height / 2) and  x == int(kernel.width / 2):
                    kernel.set_pixel(y, x, 2 - 1/(n*n))
                else:
                    kernel.set_pixel(y, x, 0 - 1/(n*n))
        print("kernel={}".format(kernel.pixels))
        result = self.filter_with_kernel(kernel)
        result.finalize()
        return  result

    def finalize(self):
        """
        Mutate self so that all of its pixel values are valid (i.e., integers
        in the range 0-255, inclusive).
        """
        self.pixels = [max(0, min(255, int(round(i)))) for i in self.pixels]

    def edges(self):
        kernel_x = Image(3, 3, [-1, 0, 1, 
                                -2, 0, 2,
                                -1, 0, 1])
        kernel_y = Image(3, 3, [-1, -2, -1,
                                 0, 0, 0,
                                 1, 2, 1])
        result = Image.new(self.width, self.height)
        O_x = self.filter_with_kernel(kernel_x)
        O_y = self.filter_with_kernel(kernel_y)
        for y in range(result.height):
            for x in range(result.width):
                color_x = O_x.get_pixel(y, x)
                color_y = O_y.get_pixel(y, x)
                O_x_y = math.sqrt(color_x ** 2 + color_y ** 2)
                result.set_pixel(y, x, O_x_y)
        result.finalize()
        return result


    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
