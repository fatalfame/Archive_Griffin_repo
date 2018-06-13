from skimage import io, data, filters
import os

filename = os.path.join(skimage.data_dir, 'moon.png')
moon = io.imread(filename)

original_image =


def channel_adjust(channel, values):
    orig_size = channel.shape
    flat_channel = channel.flatten()
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)
    return adjusted.reshape(orig_size)


r = original_image[:, :, 0]
b = original_image[:, :, 2]
r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
b_more = np.clip(b + 0.03, 0, 1.0)
merged = np.stack([r_boost_lower, original_image[:, :, 1], b_more], axis=2)
blurred = skimage.filters.gaussian(merged, sigma=10, multichannel=True)
final = np.clip(merged * 1.3 - blurred * 0.3, 0, 1.0)
b = final[:, :, 2]
b_adjusted = channel_adjust(b,
                            [0, 0.047, 0.118, 0.251, 0.318, 0.392, 0.42, 0.439, 0.475, 0.561, 0.58, 0.627, 0.671, 0.733,
                             0.847, 0.925, 1])
final[:, :, 2] = b_adjusted