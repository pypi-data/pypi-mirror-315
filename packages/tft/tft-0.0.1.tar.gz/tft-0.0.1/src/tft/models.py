from timm.models.maxxvit import TransformerBlock2d
from timm.models._efficientnet_blocks import UniversalInvertedResidual
from pytorch_ggd.GGD import DynamicGGD

class AsCAN2D(nn.Module):
    def __init__(self, input_dim, embed_dim):
        super().__init__()
        ggd=lambda num_features,**kw:DynamicGGD(num_features,True,False)
        C=lambda:UniversalInvertedResidual(embed_dim,embed_dim,act_layer=torch.nn.Identity,norm_layer=ggd)
        T=lambda:TransformerBlock2d(embed_dim,embed_dim)
        self.layers=nn.Sequential(
            nn.Conv2d(i,embed_dim,kernel_size=1),
            ggd(embed_dim),
            C(),C(),C(),T(),
            C(),C(),T(),T(),
            C(),T(),T(),T()
        )
    def forward(self,x):
        return self.layers(x)