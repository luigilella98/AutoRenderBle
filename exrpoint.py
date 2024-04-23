import Imath
import array
import OpenEXR

import numpy as np
import open3d as o3d


# extract data from exr files
f = OpenEXR.InputFile('C:/Users/luigi/Desktop/untitled1.exr')
FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
cs = list(f.header()['channels'].keys())  # channels
data = [np.array(array.array('f', f.channel(c, FLOAT))) for c in cs] 
for d in data:
    print(d.shape)
data = [d.reshape( 1920,1080) for d in data]
rgb = np.concatenate([data[i][:, :, np.newaxis] for i in [3, 2, 1]], axis=-1)
# rgb /= np.max(rgb)  # this will result in a much darker image
np.clip(rgb, 0, 1.0)  # to better visualize as HDR is not supported?

# get rgbd image
img = o3d.geometry.Image((rgb * 255).astype(np.uint8))
depth = o3d.geometry.Image((data[-1] * 1000).astype(np.uint16))
rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(img, depth, convert_rgb_to_intensity=False)

# some guessed intrinsics
intr = o3d.open3d.camera.PinholeCameraIntrinsic(1920,1080, fx=500, fy=0, cx=1920/2, cy=1080/2)

# get point cloud and visualize
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intr)
o3d.visualization.draw_geometries([pcd])