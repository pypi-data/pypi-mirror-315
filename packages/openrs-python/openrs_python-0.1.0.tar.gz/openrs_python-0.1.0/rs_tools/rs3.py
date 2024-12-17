import os
import numpy as np
from osgeo import gdal,osr
from osgeo import gdalnumeric
from osgeo.gdalconst import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image, ImageDraw
import cv2
import pyproj
from scipy.signal import convolve2d as conv2
from scipy import interpolate, ndimage
import copy

# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.


def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    a = gdalnumeric.fromstring(i.tobytes(), 'b')
    a.shape = i.im.size[1], i.im.size[0]
    return a


def arrayToImage(a):
    """
    Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    i = Image.fromstring('L', (a.shape[1], a.shape[0]),
                         (a.astype('b')).tobytes())
    return i

def pixel2world(geoMatrix, row, col):
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    
    x = ulX + col * xDist
    y = ulY + row * yDist
    
    return x,y

def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int(round(((x - ulX) / xDist),0))
    line = int(round(((ulY - y) / xDist),0))
    return (pixel, line)


def OpenArray(array, prototype_ds=None, xoff=0, yoff=0):
    ds = gdal.Open(gdalnumeric.GetArrayFilename(array))

    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open(prototype_ds)
        if prototype_ds is not None:
            gdalnumeric.CopyDatasetInfo(prototype_ds, ds, xoff=xoff, yoff=yoff)
    return ds


def histogram(a, bins=range(0, 256)):
    """
    Histogram function for multi-dimensional array.
    a = array
    bins = range of numbers to match
    """
    fa = a.flat
    n = gdalnumeric.searchsorted(gdalnumeric.sort(fa), bins)
    n = gdalnumeric.concatenate([n, [len(fa)]])
    hist = n[1:]-n[:-1]
    return hist


def stretch(a):
    """
    Performs a histogram stretch on a gdalnumeric array image.
    """
    hist = histogram(a)
    im = arrayToImage(a)
    lut = []
    for b in range(0, len(hist), 256):
        # step size
        step = reduce(operator.add, hist[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hist[i+b]
    im = im.point(lut)
    return imageToArray(im)


class LightImage():
    """
    Image class with memory efficient implementation
    """

    def __init__(self, fn):
        self.fn = fn

        # Open hyperspectral data
        self.ds = gdal.Open(fn, gdal.GA_ReadOnly)
        self.ncol = self.ds.RasterXSize
        self.nrow = self.ds.RasterYSize
        self.nband = self.ds.RasterCount

        # Determine data type used
        self.band = self.ds.GetRasterBand(1)
        self.dtype = self.band.ReadAsArray(0, 0, 1, 1).dtype
        self.gdal_dtype = self.band.DataType

        # Compute extent of the image
        self.geotransform = self.ds.GetGeoTransform()
        self.ext_up = self.geotransform[3]
        self.ext_left = self.geotransform[0]
        # Cell size
        self.x_spacing = self.geotransform[1]
        self.y_spacing = self.geotransform[5]
        # Continue computing extent
        self.ext_down = self.ext_up + self.y_spacing * self.nrow
        self.ext_right = self.ext_left + self.x_spacing * self.ncol

        # Extract projection information
        self.projection = osr.SpatialReference()
        self.projection.ImportFromWkt(self.ds.GetProjectionRef())
        
    def show_image_rgb(self, bands=[0,1,2], axis='off'):
        """
        Display rgb image
        """

        # Initialize numpy array
        img = np.zeros((self.nrow, self.ncol, 3), dtype=self.dtype)

        # Read file onto memory
        for i in bands:
            band = self.ds.GetRasterBand(i+1)
            img[:, :, i] = np.array(band.ReadAsArray(0, 0, self.ncol, self.nrow), dtype=np.uint8)

        fig = plt.figure()
        ax = fig.add_subplot(111)
            
        ax.imshow(img)
        ax.axis(axis)

        plt.show()


    def get_img_array(self):
        
        arr = np.zeros((self.nrow, self.ncol, self.nband), dtype=self.dtype)

        for i in range(self.nband):
            band = self.ds.GetRasterBand(i + 1)
            arr[:,:,i] = band.ReadAsArray(0, 0, self.ncol, self.nrow)
        return arr


    def get_intersect_image(self, img):

        if self.ext_left < img.ext_left:
            col_in,_ = world2Pixel(self.geotransform, img.ext_left, img.ext_up)
        else:
            col_in = 0
        
        if self.ext_right < img.ext_right:
            col_out = None
        else:
            col_out, _ = world2Pixel(self.geotransform, img.ext_right, img.ext_down)
            
        if self.ext_up < img.ext_up:
           row_in = 0
        else:
             _, row_in = world2Pixel(self.geotransform, img.ext_left, img.ext_up)
            
        if self.ext_down < img.ext_down:
            _, row_out = world2Pixel(self.geotransform, img.ext_right, img.ext_down)
        else:
            row_out = None

        img_arr = np.empty((self.nrow, self.ncol), dtype=np.float32)

        # get reference image extent
        ext_left = [self.ext_left, img.ext_left]
        ext_right = [self.ext_right, img.ext_right]
        ext_up = [self.ext_up, img.ext_up]
        ext_down = [self.ext_down, img.ext_down]

        # set intersection boundary
        inter_left = max(ext_left)
        inter_right = min(ext_right)
        inter_up = min(ext_up)
        inter_down = max(ext_down)
        
        # clip data with reference image extent
        #get pixel boundary
        col_start, row_start = world2Pixel(img.geotransform, inter_left, inter_up)
        col_end, row_end = world2Pixel(img.geotransform, inter_right, inter_down)
        if (col_end-col_start)<=0 or (row_end-row_start)<=0:
            return None
        # image clipping
        img_clip = img.get_box(col_start,col_end-1,row_start,row_end-1)
        
        if img_arr[row_in:row_out,col_in:col_out].shape != img_clip.shape:
            
            img_clip_resize = cv2.resize(img_clip,(img_arr[row_in:row_out,col_in:col_out].shape[1],img_arr[row_in:row_out,col_in:col_out].shape[0]),
                                         interpolation=cv2.INTER_NEAREST)
            print('Image was resized to match the dimension: ',img_clip.shape,'->',img_clip_resize.shape)
        else:
            img_clip_resize = img_clip
        
        img_arr[row_in:row_out,col_in:col_out] = img_clip_resize

        return img_arr
            
            
            
            
    def get_pixel(self, x, y, band=0):
        """
        Return the value of pixel.

        Default is to return the pixel value of first band at (x,y)

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair
        """
        # Check if given (x,y) is inside the range of the image
        if x < 0 or x > self.ncol - 1:
            print("X coordinate is out of range")
            return None

        if y < 0 or y > self.nrow - 1:
            print("Y coordinate is out of range")
            return None

        band = self.ds.GetRasterBand(band + 1)

        return band.ReadAsArray(x, y, 1, 1)[0][0]

    def get_pixel_by_coordinate(self, x, y, band=0, debug_flag=False):
        """
        Extract pixel values based on the coordinate

        (x,y) is the coordinate pair in the coordinate system used for the image.
        """

        # Check if the coordinate given is inside the image
        if (x < self.ext_left) or (x > self.ext_right) or (y < self.ext_down) or (y > self.ext_up):
            print("The given point (%f, %f) is not inside the image." % (x, y))
            return None

        # Compute offset from the upper left corner.
        x_off = x - self.ext_left
        y_off = self.ext_up - y

        x_ind = int(x_off / abs(self.x_spacing))
        y_ind = int(y_off / abs(self.y_spacing))

        if debug_flag:
            print("(x_ind, y_ind) = (%d, %d)" % (x_ind, y_ind))

        return self.img[band, y_ind, x_ind]

    def get_box(self, minx, maxx, miny, maxy, band=0):
        """
        Return the value of box.

        Default is to return the pixel value of first band

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair

        Requires (minx, maxx, miny, maxy) input

        """
        # Check if given (x,y) is inside the range of the image
        # if minx < 0 or maxx > self.ncol - 1:
        #     print("X coordinate is out of range")
        #     return None

        # if miny < 0 or maxy > self.nrow - 1:
        #     print("Y coordinate is out of range")
        #     return None
        
        if minx < 0:
            minx = 0
        
        if miny < 0:
            miny = 0
        
        if maxx > self.ncol or maxx == -1:
            maxx = self.ncol
        
        if maxy > self.nrow or maxy == -1:
            maxy = self.nrow      

        band = self.ds.GetRasterBand(band + 1)

        return band.ReadAsArray(minx, miny, maxx - minx, maxy - miny)


    def get_box_all(self, minx, maxx, miny, maxy):
        """
        Return the value of box.

        Default is to return the pixel value of first band

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair

        Requires (minx, maxx, miny, maxy) input

        """
        # Check if given (x,y) is inside the range of the image
        if minx < 0 or miny < 0:
            print("pixel coordinate is out of range")
            return None
        
        if maxx > self.ncol or maxx == -1:
            maxx = self.ncol
        
        if maxy > self.nrow or maxy == -1:
            maxy = self.nrow            
        
        num_x = int(maxx - minx)
        num_y = int(maxy - miny)


        box_img = np.zeros((self.nband, maxy-miny, maxx-minx),
                            dtype=self.dtype)

        for i in range(self.nband):
            band = self.ds.GetRasterBand(i + 1)
            box_img[i,:,:] = band.ReadAsArray(int(minx), int(miny), num_x, num_y)
            
        gt_out = [self.ext_left + minx * self.x_spacing, 
                  self.x_spacing, 
                  self.geotransform[2], 
                  self.ext_up + miny * self.y_spacing, 
                  self.geotransform[4], 
                  self.y_spacing]
        

        return box_img , gt_out

    def get_pixel_boundary(self, x, y):
        """
        Return the boundary of the specified pixel

        Will return (x_min, x_max, y_min, y_max) pair
        """
        return self.ext_left + self.x_spacing * x, self.ext_left + self.x_spacing * (x+1), \
            self.ext_up + self.y_spacing * y, self.ext_up + self.y_spacing * (y+1)

    def get_pixel_ul(self, x, y):
        return self.ext_left + self.x_spacing * x, self.ext_up + self.y_spacing * y

    def get_pixel_ll(self, x, y):
        return self.ext_left + self.x_spacing * x, self.ext_up + self.y_spacing * (y+1)

    def get_pixel_lr(self, x, y):
        return self.ext_left + self.x_spacing * (x+1), self.ext_up + self.y_spacing * (y+1)

    def get_pixel_ur(self, x, y):
        return self.ext_left + self.x_spacing * (x+1), self.ext_up + self.y_spacing * y

    def get_pixel_center(self, x, y):
        """
        Return center coordinates of the pixel

        Input: (x,y) is the image coordinate of the pixel
        """
        return self.ext_left + self.x_spacing * (x+0.5), self.ext_up + self.y_spacing * (y + 0.5)

    def get_pixel_coordinate(self, x, y):
        """
        Return pixel coordinate from the actual coordinates

        Input (x,y) is the actual coordinates, and return value will be pixel coordinates
        """
        x_off = x - self.ext_left
        y_off = y - self.ext_up

        return x_off / float(self.x_spacing), y_off / float(self.y_spacing)

    def clip_by_polygon(self, poly):
        """
        Clip image by polygon provided

        Input "poly" should be poly read by Fiona
        """
        geoTrans = self.ds.GetGeoTransform()
        points = []
        pixels = []
        pixels_clipped = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)

        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))

        # for p in poly['geometry']['coordinates'][0]:
        #     points.append(p)

        for p in points:
            pixels.append(world2Pixel(geoTrans, p[0], p[1]))

        pixels_np = np.array(pixels)
        minx = pixels_np[:, 0].min()
        maxx = pixels_np[:, 0].max()
        miny = pixels_np[:, 1].min()
        maxy = pixels_np[:, 1].max()

        # Now check if polygon is inside the image
        if (minx < 0) or (maxx > self.ncol - 1):
            print("Polygon is outside of image")
            return None

        if (miny < 0) or (maxy > self.nrow - 1):
            print("Polygon is outside of image")
            return None

        clipped_img = self.get_box_all(minx, maxx, miny, maxy)
        clipped_img_width = clipped_img.shape[2]
        clipped_img_height = clipped_img.shape[1]

        for p in pixels:
            pixels_clipped.append((p[0] - minx, p[1] - miny))

        rasterPoly = Image.new("L", (clipped_img_width, clipped_img_height), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels_clipped, 0)
        mask = imageToArray(rasterPoly)

        clipped_img_masked = gdalnumeric.choose(mask, (clipped_img, 0))

        return clipped_img_masked

    def clip_by_polygon_and_save(self, poly, out_fn):
        """
        Clip image by polygon provided

        Input "poly" should be poly read by Fiona
        """
        geoTrans = self.ds.GetGeoTransform()
        points = []
        pixels = []
        pixels_clipped = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)

        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))

        # for p in poly['geometry']['coordinates'][0]:
        #     points.append(p)

        for p in points:
            pixels.append(world2Pixel(geoTrans, p[0], p[1]))

        pixels_np = np.array(pixels)
        minx = pixels_np[:, 0].min()
        maxx = pixels_np[:, 0].max()
        miny = pixels_np[:, 1].min()
        maxy = pixels_np[:, 1].max()

        # Now check if polygon is inside the image
        if (minx < 0) or (maxx > self.ncol - 1):
            print("Polygon is outside of image")
            return None

        if (miny < 0) or (maxy > self.nrow - 1):
            print("Polygon is outside of image")
            return None

        clipped_img = self.get_box_all(minx, maxx, miny, maxy)
        clipped_img_width = clipped_img.shape[2]
        clipped_img_height = clipped_img.shape[1]

        for p in pixels:
            pixels_clipped.append((p[0] - minx, p[1] - miny))

        rasterPoly = Image.new("L", (clipped_img_width, clipped_img_height), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels_clipped, 0)
        mask = imageToArray(rasterPoly)

        clipped_img_masked = gdalnumeric.choose(mask, (clipped_img, 0))

        num_band = clipped_img_masked.shape[0]

        clipped_lc = self.ext_left + minx * self.x_spacing
        clipped_uc = self.ext_up   + miny * self.y_spacing

        driver = gdal.GetDriverByName('ENVI')
        outds = driver.Create(out_fn, clipped_img_width, clipped_img_height,
                            clipped_img_masked.shape[0], self.gdal_dtype)
        outds.SetGeoTransform([clipped_lc, self.x_spacing, self.geotransform[2],
                clipped_uc, self.geotransform[4], self.y_spacing])
        outds.SetProjection(self.ds.GetProjection())

        if num_band == 1:
            outds.GetRasterBand(1).WriteArray(clipped_img_masked[:,:])
        else:
            for i in range(num_band):
                outds.GetRasterBand(i+1).WriteArray(clipped_img_masked[i,:,:])

        outds = None
        
    def create_copy(self, out_fn, projection=None, gt=None):
        
        if projection is None:
            projection = self.projection
        if gt is None:
            gt = self.geotransform
            
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.CreateCopy(out_fn, self.ds, 0)
        out_ds.SetProjection(projection)
        out_ds.SetGeoTransform(gt)
        out_ds = None
        

class RSImage(object):
    """
    Image class

    This class is initialized by opening file and load it onto memory.
    Below information is updated after initialization

    self.ncol : Number of columns
    self.nrow : Number of row
    self.nband :Number of band
    self.dtype : Data type
    self.img : Numpy array contains remote sensing data
    """

    def __init__(self, fn):
        self.fn = fn

        # Open hyperspectral data
        self.ds = gdal.Open(fn, gdal.GA_ReadOnly)
        self.ncol = self.ds.RasterXSize
        self.nrow = self.ds.RasterYSize
        self.nband = self.ds.RasterCount

        # Determine data type used
        self.band = self.ds.GetRasterBand(1)
        self.dtype = self.band.ReadAsArray(0, 0, 1, 1).dtype

        # Initialize numpy array
        self.img = np.zeros((self.nband, self.nrow, self.ncol), dtype=self.dtype)

        # Read file onto memory
        for i in range(self.nband):
            self.band = self.ds.GetRasterBand(i+1)
            self.img[i, :, :] = self.band.ReadAsArray(0, 0, self.ncol, self.nrow)

        # Compute extent of the image
        self.geotransform = self.ds.GetGeoTransform()
        self.ext_up = self.geotransform[3]
        self.ext_left = self.geotransform[0]
        # Cell size
        self.x_spacing = self.geotransform[1]
        self.y_spacing = self.geotransform[5]
        # Continue computing extent
        self.ext_down = self.ext_up + self.y_spacing * self.nrow
        self.ext_right = self.ext_left + self.x_spacing * self.ncol

    def normalize(self):
        """
        Normalize Image

        Make each band to have mean = 0 & std = 1

        Use Z = \frac{X - \mu}{\sigma}
        """
        # Initialize numpy array for normalized image
        self.norm_img = np.zeros((self.nband, self.nrow, self.ncol), dtype=np.float32)

        for i in np.arange(self.nband):
            # Make a pointer for easy typing
            cur = self.img[i, :, :]
            # Find out NaN Cell
            nan_cond = np.isnan(cur)
            cond = np.invert(nan_cond)
            # Extract only none nan Cell
            good_cur = cur[cond]
            self.norm_img[i, cond] = (good_cur - good_cur.mean()) / good_cur.std()
            self.norm_img[i, nan_cond] = cur[nan_cond]

    def norm_tofile(self, outfn, outfmt="ENVI"):
        """
        Save normalized data to file
        """
        driver = gdal.GetDriverByName(outfmt)
        ds = driver.Create(outfn, self.ncol, self.nrow, self.nband, gdal.GDT_Float32)

        proj = self.ds.GetProjection()
        geot = self.ds.GetGeoTransform()
        meta = self.ds.GetMetadata()

        ds.SetProjection(proj)
        ds.SetGeoTransform(geot)
        ds.SetMetadata(meta)

        for i in np.arange(self.nband):
            band = ds.GetRasterBand(i+1)
            band.WriteArray(self.norm_img[i, :, :])

        ds = None

    def get_pixel(self, x, y, band=0):
        """
        Return the value of pixel.

        Default is to return the pixel value of first band at (x,y)

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair
        """
        # Check if given (x,y) is inside the range of the image
        if x < 0 or x > self.ncol - 1:
            print("X coordinate is out of range")
            return None

        if y < 0 or y > self.nrow - 1:
            print("Y coordinate is out of range")
            return None

        return self.img[band, y, x]

    def get_pixel_all_band(self, x, y):
        """
        Return the value of pixel with all band as numpy array.

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair.
        """
        # Check if given (x,y) is inside the range of the image
        if x < 0 or x > self.ncol - 1:
            print("X coordinate is out of range")
            return None

        if y < 0 or y > self.nrow - 1:
            print("Y coordinate is out of range")
            return None

        return self.img[:, y, x]

    def print_extent(self):
        """
        Print extent of the image
        """

        print("(x_min, x_max) = (%f, %f)" % (self.ext_left, self.ext_right))
        print("(y_min, y_max) = (%f, %f)" % (self.ext_down, self.ext_up))

    def extract_pixel_by_coordinate(self, x, y, debug_flag=False):
        """
        Extract pixel values based on the coordinate

        (x,y) is the coordinate pair in the coordinate system used for the image.
        """

        # Check if the coordinate given is inside the image
        if (x < self.ext_left) or (x > self.ext_right) or (y < self.ext_down) or (y > self.ext_up):
            # print ("The given point (%f, %f) is not inside the image." % (x,y))
            # self.print_extent()
            return None

        # Compute offset from the upper left corner.
        x_off = x - self.ext_left
        y_off = self.ext_up - y

        x_ind = int(x_off / abs(self.x_spacing))
        y_ind = int(y_off / abs(self.y_spacing))

        if debug_flag:
            print("(x_ind, y_ind) = (%d, %d)" % (x_ind, y_ind))

        return self.img[:, y_ind, x_ind]

    def get_xy_by_coordinate(self, x, y):
        """
        Return column and row index from the given coordinates

        (x,y) is the coordinate pair in the coordinate system used for the image.
        """

        # Check if the coordinate given is inside the image
        if (x < self.ext_left) or (x > self.ext_right) or (y < self.ext_down) or (y > self.ext_up):
            #print ("The given point (%f, %f) is not inside the image." % (x,y))
            # self.print_extent()
            return None, None

        # Compute offset from the upper left corner.
        x_off = x - self.ext_left
        y_off = self.ext_up - y

        x_ind = int(x_off / abs(self.x_spacing))
        y_ind = int(y_off / abs(self.y_spacing))

        return x_ind, y_ind

    def show_image(self, band=1, cmap=cm.gist_heat):
        """
        Display image of specified band.
        Default band to display is first band
        """

        fig = plt.figure()
        ax = fig.add_subplot(111)

        cax = ax.imshow(self.img[band-1, :, :], cmap=cmap, interpolation='nearest')
        ax.axis('off')
        cbar = fig.colorbar(cax)

        plt.show()
        
        
    def show_image_rgb(self):
        """
        Display rgb image
        """

        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        img = self.img[:3,:,:]
            
        img = np.swapaxes(img,0,1)
        img = np.swapaxes(img,1,2)

        ax.imshow(img)
        ax.axis('off')

        plt.show()
        

    def get_pixel_center_coordinates(self, x_ind, y_ind):
        """
        Return center coordinate of the pixel given by (x_ind, y_ind)

        Input: x_ind, y_ind (this is zero based index)
        Output: (x,y) center coordinates of the pixel
        """

        if (x_ind < 0) or (x_ind > self.ncol - 1):
            print("X index is out of range")
            return None, None

        if (y_ind < 0) or (y_ind > self.nrow - 1):
            print("Y index is out of range")
            return None, None

        x_center = self.ext_left + x_ind * self.x_spacing + 0.5 * self.x_spacing
        y_center = self.ext_up + y_ind * self.y_spacing + 0.5 * self.y_spacing

        return x_center, y_center

    def get_pixel_center_coordinates(self, x_ind, y_ind):
        """
        Get center coordinates of the pixel
        """
        x_coord = self.ext_left + x_ind * self.x_spacing + self.x_spacing / 2.0
        y_coord = self.ext_up + y_ind * self.y_spacing + self.y_spacing / 2.0

        return x_coord, y_coord

    def clip_by_polygon(self, poly):
        """
        Clip image by polygon provided

        Input "poly" should be poly read by Fiona
        """
        geoTrans = self.ds.GetGeoTransform()
        points = []
        pixels = []
        pixels_clipped = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)

        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))

        # for p in poly['geometry']['coordinates'][0]:
        #     points.append(p)

        for p in points:
            pixels.append(world2Pixel(geoTrans, p[0], p[1]))

        pixels_np = np.array(pixels)
        minx = pixels_np[:, 0].min()
        maxx = pixels_np[:, 0].max()
        miny = pixels_np[:, 1].min()
        maxy = pixels_np[:, 1].max()

        # Now check if polygon is inside the image
        if (minx < 0) or (maxx > self.ncol - 1):
            print("Polygon is outside of image")
            return None

        if (miny < 0) or (maxy > self.nrow - 1):
            print("Polygon is outside of image")
            return None

        clipped_img = self.img[:, miny:maxy, minx:maxx]
        clipped_img_width = clipped_img.shape[2]
        clipped_img_height = clipped_img.shape[1]

        for p in pixels:
            pixels_clipped.append((p[0] - minx, p[1] - miny))

        rasterPoly = Image.new("L", (clipped_img_width, clipped_img_height), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels_clipped, 0)
        mask = imageToArray(rasterPoly)

        clipped_img_masked = gdalnumeric.choose(mask, (clipped_img, 0))

        return clipped_img_masked


class ImageArray():
    """
    ImageArray class designed for dealing numpy array as Image
    """

    def __init__(self, data):
        self.data = data

    def set_box_coordinate_utm(self, up, left, spatial_resolution, num_row, num_col, utm_zone_number, utm_ns_code=1):
        self.up = up
        self.left = left
        self.spatial_resolution = spatial_resolution
        self.num_row = num_row
        self.num_col = num_col
        self.zone_number = utm_zone_number
        self.ns_code = utm_ns_code

    def tofile_utm(self, out_fn):
        out_format = "ENVI"

        driver = gdal.GetDriverByName(out_format)
        # Number of bands
        nob = self.data.shape[0]

        if self.data.dtype == np.uint8:
            outds = driver.Create(out_fn, self.num_col, self.num_row, nob, gdal.GDT_Byte)
        if self.data.dtype == np.int16:
            outds = driver.Create(out_fn, self.num_col, self.num_row, nob, gdal.GDT_Int16)
        elif self.data.dtype == np.int32:
            outds = driver.Create(out_fn, self.num_col, self.num_row, nob, gdal.GDT_Int32)
        elif self.data.dtype == np.float32:
            outds = driver.Create(out_fn, self.num_col, self.num_row, nob, gdal.GDT_Float32)
        elif self.data.dtype == np.float64:
            outds = driver.Create(out_fn, self.num_col, self.num_row, nob, gdal.GDT_Float64)

        outds.SetGeoTransform([self.left, self.spatial_resolution, 0,
                               self.up, 0, -self.spatial_resolution])

        srs = osr.SpatialReference()
        # UTM Zone information
        srs.SetUTM(self.zone_number, self.ns_code)
        # Datum
        srs.SetWellKnownGeogCS('WGS84')
        outds.SetProjection(srs.ExportToWkt())

        for i in range(nob):
            outds.GetRasterBand(i+1).WriteArray(self.data[i, :, :])

        outds = None

    def tofile_with_specification(self, out_fn, geo_transform, projection_ref, out_format="GTiff"):
        nob = self.data.shape[0]
        driver = gdal.GetDriverByName(out_format)

        # Determine data type
        if self.data.dtype == np.int16:
            outds = driver.Create(
                out_fn, self.data.shape[2], self.data.shape[1], nob, gdal.GDT_Int16)
        elif self.data.dtype == np.int32:
            outds = driver.Create(
                out_fn, self.data.shape[2], self.data.shape[1], nob, gdal.GDT_Int32)
        elif self.data.dtype == np.float32:
            outds = driver.Create(
                out_fn, self.data.shape[2], self.data.shape[1], nob, gdal.GDT_Float32)
        elif self.data.dtype == np.float64:
            outds = driver.Create(
                out_fn, self.data.shape[2], self.data.shape[1], nob, gdal.GDT_Float64)
        elif self.data.dtype == np.uint8:
            outds = driver.Create(
                out_fn, self.data.shape[2], self.data.shape[1], nob, gdal.GDT_Byte)

        outds.SetGeoTransform(geo_transform)

        #srs = osr.SpatialReference()
        # UTM Zone information
        # srs.SetUTM(self.zone_number,self.ns_code)
        # Datum
        # srs.SetWellKnownGeogCS('WGS84')
        outds.SetProjection(projection_ref.ExportToWkt())

        for i in range(nob):
            outds.GetRasterBand(i+1).WriteArray(self.data[i, :, :])

        outds = None

    def tofile_as_other_image(self, out_fn, other_image):
        """
        Save numpy array as image when I already have other image file which has exactly same geospatial settings

        other_image must be GDAL object

        Only geospatial information is coming from the other_image, but data type is determined by the data type of numpy array (Only np.int16, np.int32, np.float32, np.float64 are supported right now)
        """
        # Determine number of bands
        nob = self.data.shape[0]

        out_format = "ENVI"

        driver = gdal.GetDriverByName(out_format)

        # Determine data type
        if self.data.dtype == np.uint8:
            outds = driver.Create(out_fn, other_image.ds.RasterXSize,
                                  other_image.ds.RasterYSize, nob, gdal.GDT_Byte)
        if self.data.dtype == np.int16:
            outds = driver.Create(out_fn, other_image.ds.RasterXSize,
                                  other_image.ds.RasterYSize, nob, gdal.GDT_Int16)
        elif self.data.dtype == np.int32:
            outds = driver.Create(out_fn, other_image.ds.RasterXSize,
                                  other_image.ds.RasterYSize, nob, gdal.GDT_Int32)
        elif self.data.dtype == np.float32:
            outds = driver.Create(out_fn, other_image.ds.RasterXSize,
                                  other_image.ds.RasterYSize, nob, gdal.GDT_Float32)
        elif self.data.dtype == np.float64:
            outds = driver.Create(out_fn, other_image.ds.RasterXSize,
                                  other_image.ds.RasterYSize, nob, gdal.GDT_Float64)

        outds.SetGeoTransform(other_image.ds.GetGeoTransform())

        #srs = osr.SpatialReference()
        # UTM Zone information
        # srs.SetUTM(self.zone_number,self.ns_code)
        # Datum
        # srs.SetWellKnownGeogCS('WGS84')
        outds.SetProjection(other_image.ds.GetProjection())

        for i in range(nob):
            outds.GetRasterBand(i+1).WriteArray(self.data[i, :, :])

        outds = None


def find_intercept(p1, p2):
    """
    Find intercept between p1 and p2

    Finding is based on every integer grid

    Example: between 0.2 and 2.4 -> Find (1, 2)

    p1 = (x1, y1)
    p2 = (x2, y2)

    This function is only for RS image, so negative image coordinate does not make sense.
    Any negative image coordinate will be set to zero automatically.
    """

    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    # Make any negative to zero
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 < 0:
        x2 = 0
    if y2 < 0:
        y2 = 0

    # Make x1 smaller than x2, same for y
    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp

    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp

    xlist = range(int(x1)+1, int(x2)+1)
    ylist = range(int(y1)+1, int(y2)+1)

    point_list = []

    for temp_x in xlist:
        temp_y = find_y(p1, p2, temp_x)
        point_list.append((temp_x, temp_y))

    for tempY in ylist:
        tempX = find_x(p1, p2, tempY)
        point_list.append((tempX, tempY))

    return point_list


def find_y(p1, p2, x):
    """
    Find y value for given x coordinate for line between p1 and p2

    Based on below formular

    y - y1 = (y2 - y1) / (x2 - x2) * (x - x1)
    """
    return (p2[1] - p1[1]) / (p2[0] - p1[0]) * (x - p1[0]) + p1[1]


def find_x(p1, p2, y):
    """
    Find y value for given x coordinate for line between p1 and p2

    Based on below formular

    y - y1 = (y2 - y1) / (x2 - x2) * (x - x1)
    """
    return (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]


def image_resample(img, ratio):
    """
    Resample image

    img: 2D numpy array
    ratio: ratio to resample (2: means average 4 pixels to 1 pixel)
    """
    if len(img.shape) != 2:
        print("Input image must be 2D numpy array")
        return None

    nrow = img.shape[0] / ratio
    ncol = img.shape[1] / ratio

    # Results array
    out_img = np.zeros((nrow, ncol), dtype=img.dtype)

    for i in xrange(nrow):
        row_start = i * ratio
        row_end = (i+1) * ratio

        for j in xrange(ncol):
            col_start = j * ratio
            col_end = (j+1) * ratio

            out_img[i, j] = img[row_start:row_end, col_start:col_end].mean()

    return out_img


def save_tiff_meta(out_fn, ds_array, projection, gt, etype=np.float64):
    driver = gdal.GetDriverByName('GTiff')
    
    if etype==np.uint8:
        out_etype=gdal.GDT_Byte
    elif etype==np.float64:
        out_etype=gdal.GDT_Float64
    
    out_ds = driver.Create(out_fn,np.shape(ds_array)[1],np.shape(ds_array)[0],1,out_etype)
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(projection)
    for i in range(np.shape(ds_array)[2]):
        out_ds.GetRasterBand(i+1).WriteArray(ds_array[:,:,i])
    out_ds = None
    
    
def save_jpeg(out_fn, ds_array, projection, gt):
    driver = gdal.GetDriverByName('JPEG')
    out_ds = driver.Create(out_fn,np.shape(ds_array)[1],np.shape(ds_array)[0],1,gdal.GDT_Byte)
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(projection)
    for i in range(np.shape(ds_array)[2]):
        out_ds.GetRasterBand(i+1).WriteArray(ds_array[:,:,i])
    out_ds = None
    

def save_map(map_fn, src, ncol, nrow, target_epsg, geotransform, bands=1, eType=gdal.GDT_Float32, format='GTiff', set_no_data_val=False):
    driver = gdal.GetDriverByName(format)
    map_ds = driver.Create(map_fn, xsize = ncol, ysize = nrow, bands = bands, eType=eType)
    wkt = pyproj.CRS.from_epsg(target_epsg).to_wkt()
    map_ds.SetProjection(wkt)
    map_ds.SetGeoTransform(geotransform)
    map_ds.GetRasterBand(1).WriteArray(src)
    if set_no_data_val != False:
        map_ds.GetRasterBand(1).SetNoDataValue(set_no_data_val)
    map_ds = None
    
    
    
def sobel_filter(img):
    Gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
    Gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])

    rows, columns = np.shape(img)  # we need to know the shape of the input grayscale image
    sobel_filtered_image = np.zeros(shape=(rows, columns))  # initialization of the output image array (all elements are 0)

    # Now we "sweep" the image in both x and y directions and compute the output

    gx = conv2(img, Gx, boundary='symm', mode='same')
    gy = conv2(img, Gy, boundary='symm', mode='same')
    sobel_filtered_image = np.sqrt(gx ** 2 + gy ** 2)

    return sobel_filtered_image


def scipy_interpolation(img, METHOD):
    x = np.arange(0, img.shape[1])
    y = np.arange(0, img.shape[0])
    # mask invalid values
    img = np.ma.masked_invalid(img)
    xx, yy = np.meshgrid(x, y)
    # get only the valid values
    x1 = xx[~img.mask]
    y1 = yy[~img.mask]
    newarr = img[~img.mask]

    interpolated_img = interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method=METHOD)

    return interpolated_img


def interpolation(img, SCALE=5, interpolation_method='linear'):

    dtm_temp = scipy_interpolation(img[::SCALE,::SCALE], METHOD=interpolation_method)
    dtm_temp = ndimage.zoom(dtm_temp, SCALE, order=0)
    NEW_VALUE_FOR_NAN = np.multiply(np.isnan(img),dtm_temp)

    REPLACE_NAN_WITH_ZERO = copy.deepcopy(img)
    REPLACE_NAN_WITH_ZERO[np.isnan(img)]=0

    interpolated_img = REPLACE_NAN_WITH_ZERO+NEW_VALUE_FOR_NAN
    return interpolated_img
