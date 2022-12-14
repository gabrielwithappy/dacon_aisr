import torch
from torch import nn as nn
from torch.nn import functional as F

from basicsr.utils.registry import ARCH_REGISTRY
from basicsr.archs.arch_util import default_init_weights, make_layer, pixel_unshuffle


class ResidualDenseBlock(nn.Module):
    """Residual Dense Block.
    Used in RRDB block in ESRGAN.
    Args:
        num_feat (int): Channel number of intermediate features.
        num_grow_ch (int): Channels for each growth.
    """

    def __init__(self, num_feat=64, num_grow_ch=32):
        super(ResidualDenseBlock, self).__init__()
        self.conv1 = nn.Conv2d(num_feat, num_grow_ch, 3, 1, 1)
        self.conv2 = nn.Conv2d(num_feat + num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv3 = nn.Conv2d(num_feat + 2 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv4 = nn.Conv2d(num_feat + 3 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv5 = nn.Conv2d(num_feat + 4 * num_grow_ch, num_feat, 3, 1, 1)

        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

        # initialization
        default_init_weights([self.conv1, self.conv2, self.conv3, self.conv4, self.conv5], 0.1)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        # Empirically, we use 0.2 to scale the residual for better performance
        return x5 * 0.2 + x


class RRDB(nn.Module):
    """Residual in Residual Dense Block.
    Used in RRDB-Net in ESRGAN.
    Args:
        num_feat (int): Channel number of intermediate features.
        num_grow_ch (int): Channels for each growth.
    """
    
    def __init__(self, num_feat, num_grow_ch=32):
        super(RRDB, self).__init__()
        self.rdb1 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb2 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb3 = ResidualDenseBlock(num_feat, num_grow_ch)
        print("Self Ensemble Model")

    def forward(self, x):
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)
        # Empirically, we use 0.2 to scale the residual for better performance
        return out * 0.2 + x


@ARCH_REGISTRY.register()
class RRDBNetRot(nn.Module):
    """Networks consisting of Residual in Residual Dense Block, which is used
    in ESRGAN.
    ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks.
    We extend ESRGAN for scale x2 and scale x1.
    Note: This is one option for scale 1, scale 2 in RRDBNet.
    We first employ the pixel-unshuffle (an inverse operation of pixelshuffle to reduce the spatial size
    and enlarge the channel size before feeding inputs into the main ESRGAN architecture.
    Args:
        num_in_ch (int): Channel number of inputs.
        num_out_ch (int): Channel number of outputs.
        num_feat (int): Channel number of intermediate features.
            Default: 64
        num_block (int): Block number in the trunk network. Defaults: 23
        num_grow_ch (int): Channels for each growth. Default: 32.
    """

    def __init__(self, num_in_ch, num_out_ch, scale=4, num_feat=64, num_block=23, num_grow_ch=32):
        super(RRDBNetRot, self).__init__()
        self.scale = scale
        if scale == 2:
            num_in_ch = num_in_ch * 4
        elif scale == 1:
            num_in_ch = num_in_ch * 16
        self.conv_first = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1)
        self.body = make_layer(RRDB, num_block, num_feat=num_feat, num_grow_ch=num_grow_ch)
        self.conv_body = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        # upsample
        self.conv_up1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_hr = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_last = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)

        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def _forward(self, x):
        if self.scale == 2:
            feat = pixel_unshuffle(x, scale=2)
        elif self.scale == 1:
            feat = pixel_unshuffle(x, scale=4)
        else:
            feat = x
        feat = self.conv_first(feat)
        body_feat = self.conv_body(self.body(feat))
        feat = feat + body_feat
        # upsample
        feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode='nearest')))
        feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode='nearest')))
        out = self.conv_last(self.lrelu(self.conv_hr(feat)))
        return out
    
    def _get_rotateds(self, x):
        x90 = torch.rot90(x, k=1, dims=(2, 3))
        x180 = torch.rot90(x, k=2, dims=(2, 3))
        x270 = torch.rot90(x, k=3, dims=(2, 3))
        x_flip = torch.flip(x, dims=(3,))
        x_flip90 = torch.rot90(x_flip, k=1, dims=(2, 3))
        x_flip180 = torch.rot90(x_flip, k=2, dims=(2, 3))
        x_flip270 = torch.rot90(x_flip, k=3, dims=(2, 3))
        print("finish applying geometric arguments to input data")        
        return (x, x90, x180, x270, x_flip, x_flip90, x_flip180, x_flip270)
       
    def _get_derotateds(self, xs):
        x, x90, x180, x270, x_flip, x_flip90, x_flip180, x_flip270 = xs
        x90 = torch.rot90(x90, k=3, dims=(2, 3))
        x180 = torch.rot90(x180, k=2, dims=(2, 3))
        x270 = torch.rot90(x270, k=1, dims=(2, 3))
        x_flip = torch.flip(x_flip, dims=(3,))
        x_flip90 = torch.rot90(x_flip90, k=3, dims=(2, 3))
        x_flip90 = torch.flip(x_flip90, dims=(3,))
        x_flip180 = torch.rot90(x_flip180, k=2, dims=(2, 3))
        x_flip180 = torch.flip(x_flip180, dims=(3,))
        x_flip270 = torch.rot90(x_flip270, k=1, dims=(2, 3))
        x_flip270 = torch.flip(x_flip270, dims=(3,))
        print("finish restoring geometric arguments to input data")                
        return (x, x90, x180, x270, x_flip, x_flip90, x_flip180, x_flip270)
        
    def forward(self, x):
        xs = self._get_rotateds(x)
        ys = []
        for x in xs:
            y = self._forward(x)
            ys.append(y)
        ys = self._get_derotateds(ys)
        ys = torch.stack(ys, dim=0)
        #y = torch.mean(ys, dim=0)
        y = torch.median(ys, dim=0).values
        return y