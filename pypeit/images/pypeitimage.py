""" Simple object to hold + process a single image.
"""

from pypeit import msgs
from pypeit import ginga

import numpy as np

from astropy.io import fits

from pypeit.core import save
from pypeit.images import maskimage
from pypeit.io import initialize_header
from pypeit import datamodel

from IPython import embed

from importlib import reload
reload(datamodel)



class PypeItImage(datamodel.DataContainer, maskimage.ImageMask):
    """
    Class to hold a single image from a single detector in PypeIt
    and its related images (e.g. ivar, mask).

    Oriented in its spec,spat format

    The intent is to keep this object as light-weight as possible.

    Args:
        image (np.ndarray):
        ivar (np.ndarray, optional):
        rn2img (np.ndarray, optional):
        bpm (np.ndarray, optional):
        binning (tuple, optional):
        crmask (np.ndarray, optional):
        mask (np.ndarray, optional):

    Attributes:
        head0 (astropy.io.fits.Header):

    """
    # Set the version of this class
    version = '1.0.0'
    #
    datamodel = {
        'image': dict(otype=np.ndarray, atype=np.floating, desc='Main data image'),
        'ivar': dict(otype=np.ndarray, atype=np.floating, desc='Main data inverse variance image'),
        'rn2img': dict(otype=np.ndarray, atype=np.floating, desc='Read noise squared image'),
        'bpm': dict(otype=np.ndarray, atype=np.integer, desc='Bad pixel mask'),
        'crmask': dict(otype=np.ndarray, atype=np.integer, desc='CR mask image'),
        'mask': dict(otype=np.ndarray, atype=np.integer, desc='Full mask'),
        'BIN_SPEC': dict(otype=(int, np.integer), desc='Binning in spectral dimension'),
        'BIN_SPAT': dict(otype=(int, np.integer), desc='Binning in spatial dimension'),
        'HEAD0': dict(otype=fits.header.Header, desc='Image header of primary HDU'),
    }

    @classmethod
    def from_file(cls, file):
        """
        Instantiate from a file on disk (FITS file)

        Args:
            file (str):

        Returns:
            :class:`pypeit.images.pypeitimage.PypeItImage`:
                Loaded up PypeItImage with the primary Header attached

        """
        slf = super(PypeItImage, cls).from_file(file)

        # Open
        hdul = fits.open(file)
        # Header
        slf.HEAD0 = hdul[0].header
        # Return
        return slf

    def __init__(self, image, ivar=None, rn2img=None, bpm=None,
                 binning=None, crmask=None, mask=None):

        # Internals
        maskimage.ImageMask.__init__(self, bpm)
        self.binning = binning

        # Setup the DataContainer
        super(PypeItImage, self).__init__({'image': image})

        # Optional Attributes
        if ivar is not None:
            self.ivar = ivar
        if rn2img is not None:
            self.rn2img = rn2img
        #self.head0 = None

        # Mask attributes
        if crmask is not None:
            self.crmask = crmask
        if mask is not None:
            self.mask = mask

        # Data model
        #self.allowed_attributes = ('image', 'ivar', 'rn2img') + self.mask_attributes

    '''
    # TODO -- Instantiate these methods by making a DataModel class
    #   Have a child for data as a Table instead of a dict
    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):

        if not '_PypeItImage__initialised' in self.__dict__:  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif item in self.__dict__:       # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __setitem__(self, item, value):
        if item not in data_model.keys():
            raise IOError("Cannot set {} attribute.  It is not in the data model".format(item))
        if not isinstance(value, data_model[item]['otype']):
            print("Wrong data type for attribute: {}".format(item))
            print("Allowed type(s) are: {}".format(data_model[item]['otype']))
            raise IOError("Try again")
        # Array?
        if 'atype' in data_model[item].keys():
            if not isinstance(value.flat[0], data_model[item]['atype']):
                print("Wrong data type for array: {}".format(item))
                print("Allowed type(s) for the array are: {}".format(data_model[item]['atype']))
                raise IOError("Try again")
        # Set
        self._data[item] = value

    def __getitem__(self, item):
        if item in self._data.keys():
            return self._data[item]
        else:
            raise KeyError
    '''


    @property
    def shape(self):
        return () if self.image is None else self.image.shape

    def write(self, outfile, hdr=None, iext=None):
        """
        Write the image(s) to a multi-extension FITS file

        Note: This method cannot be named "save" as it would conflict
        with the imported module

        Extensions will be:
           PRIMARY
           IMAGE
           IVAR (optional)
           MASK (optional)

        Args:
            outfile:
            iext (str, optional):
                Name for the first extension
                Defaults to IMAGE
            hdr (`astropy.io.fits.Header`, optional):
                The header to write

        """
        # TODO -- Should we use the internal HEAD0 if that exists??
        if hdr is None:
            hdr = initialize_header()

        # Chk
        if not hasattr(self, 'image'):
            msgs.warn("Image is not ready to save.")
            return

        # Save whatever is available
        data = [self.image]
        if iext is None:
            ext = ['image']
        else:
            ext = [iext]

        # Work on the rest
        for item in ['ivar', 'mask']:
            if hasattr(self, item) and getattr(self,item) is not None:
                data.append(getattr(self, item))
                ext.append(item)

        # A few more bits
        hdr['FLAVOR'] = self.__class__.__name__
        hdr['VERSDM'] = self.version

        # TODO -- Default to float32 for float images?
        # Write the fits file
        save.write_fits(hdr, data, outfile, extnames=ext)

    def show(self):
        """
        Show the image in a ginga viewer.
        """
        if self.image is None:
            # TODO: This should fault.
            msgs.warn("No image to show!")
            return
        ginga.show_image(self.image, chname='image')

    def __repr__(self):
        repr = '<{:s}: '.format(self.__class__.__name__)
        # Image
        rdict = {}
        for attr in ['image', 'ivar', 'rn2img', 'crmask', 'mask']:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                rdict[attr] = True
            else:
                rdict[attr] = False
        repr += ' images={}'.format(rdict)
        repr = repr + '>'
        return repr

