# To import the library directly:
# from bfbridge._bfbridge import ffi, lib
# Or import the wrapper only:
import bfbridge
# TODO: Add dot
from WSIImageHandle import WSIImageHandle
import numpy as np
from typing import Union

class BioFormatsHandle(WSIImageHandle):
    def __init__(self, fname):
        self.bflibrary = bfbridge.BFBridgeThread()
        self.bfinstance = bfbridge.BFBridgeInstance(self.bflibrary)

        if self.bfinstance.open(fname) != 1:
            print(self.bfinstance.get_error_string())
            return

        self._mpp_x = self.get_mpp_x()
        self._mpp_y = self.get_mpp_y()
        
        # get magnification factor
        mpp = self._mpp_x if self._mpp_x > 0 else None
        if mpp:
            self._magnification_factor = round(1 / mpp * 10, -1)
        else:
            self._magnification_factor = None
        
        # The number of levels in the slide. Levels are numbered from 0
        self._level_count = self.bfinstance.get_resolution_count()

        # A list of (width, height) tuples, one for each level of the slide. level_dimensions[k] are the dimensions of level k.
        self._level_dimensions = []
        for i in range(self._level_count):
            self.set_current_resolution(i)
            self._level_dimensions.append( \
                (self.bfinstance.get_size_x(), self.bfinstance.get_size_y()))
            
        self.width, self_height = self._level_dimensions[0]

        # A list of downsample factors for each level of the slide. level_downsamples[k] is the downsample factor of level k.
        self._level_downsamples = [self._level_dimensions[0][0] / dim[0] for dim in self._level_dimensions]

        self._has_bounding_box = False
        self._bounding_box = (0, 0, self.width, self.height)


    @property
    def has_bounding_box(self):
        return self._has_bounding_box

    # using #ffffff as default background color
    @property
    def background_color(self):
        return "#ffffff"
        
    @property
    def bounding_box(self):
        return self._bounding_box

    @property
    def dimensions(self):
        return (self.width, self.height) 

    @property
    def magnification(self) -> Union[float, None]:
        return self._magnification_factor

    @property
    def level_count(self):
        return self._level_count

    @property
    def level_dimensions(self):
        return self._level_dimensions

    @property
    def level_downsamples(self):
        return self._level_downsamples

    @property
    def vendor(self):
        return self.bfinstance.get_format()

    @property
    def mpp_x(self):
        return self._mpp_x

    @property
    def mpp_y(self):
        return self._mpp_y
    
    # TODO
    @property
    def comment(self):
        return "BioFormats - comment #TODO"
    
    @property
    def bounding_box(self):
        return super().bounding_box    

    def get_thumbnail(self, new_dim):
        raise ValueError("not implemented")

    def get_best_level_for_downsample(self, down_factor):
        return np.argmin(np.abs(np.asarray(self._level_downsamples) - down_factor))
            
    def read_region(self, location, level, size):
        return self.osh.read_region(location, level, size)
    
    def read_label(self):
        raise ValueError("not implemented")

    def read_macro(self):
        raise ValueError("not implemented")
