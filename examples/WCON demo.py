# -*- coding: utf-8 -*-
"""
Demonstrates loading and saving to a WCON file

"""
import sys
import os
import warnings

# We must add .. to the path so that we can perform the
# import of open_worm_analysis_toolbox while running this as
# a top-level script (i.e. with __name__ = '__main__')
sys.path.append('..')
import open_worm_analysis_toolbox as mv

import wcon
import pandas as pd

class BasicWorm2(wcon.WCONWorms):
    pass

if __name__ == '__main__':
    warnings.filterwarnings('error')

    base_path = os.path.abspath(
        mv.user_config.EXAMPLE_DATA_PATH)
    schafer_bw_file_path = \
        os.path.join(base_path,
                     "example_contour_and_skeleton_info.mat")
    bw = mv.BasicWorm.from_schafer_file_factory(
        schafer_bw_file_path)

    with open('testfile.wcon', 'w') as f:
        f.write('{\n    {"units":"t":"s","x":"mm","y":"mm"},\n    {"data":[{')
        num_timeframes = len(bw.h_dorsal_contour)
        f.write('"t":%s,' % str(list(range(num_timeframes))))
        f.write('\n"x":[')
        for frame_index in range(10): #num_timeframes):
            f.write('%s,' % repr(bw.h_dorsal_contour))
        f.write(']}]}}')
        
    #for bw.h_skeleton

    #nw = mv.NormalizedWorm.from_BasicWorm_factory(bw)

    #wp = mv.NormalizedWormPlottable(nw, interactive=False)

    # wp.show()

    # TODO:
    # bw.save_to_wcon('test.wcon')
    #bw2 = mv.BasicWorm.load_from_wcon('test.wcon')

    #assert(bw == bw2)


def main2():
    base_path = os.path.abspath(
        mv.user_config.EXAMPLE_DATA_PATH)

    JSON_path = os.path.join(base_path, 'test.JSON')

    b = mv.BasicWorm()
    #b.contour[0] = 100.2
    #b.metadata['vulva'] = 'CCW'
    b.save_to_JSON(JSON_path)

    c = mv.BasicWorm()
    c.load_from_JSON(JSON_path)
    print(c.contour)

    # dat.save_to_JSON(JSON_path)
