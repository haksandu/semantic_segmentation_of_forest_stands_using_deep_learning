
from matplotlib import pyplot as plt


def plot_spectral_bands(image):
    num_bands = image.shape[2]
    fig, axes = plt.subplots(1, num_bands, figsize=(4*num_bands, 4))
    
    for i in range(num_bands):
        axes[i].imshow(image[:, :, i], cmap='gray')  # Plot each band
        axes[i].set_title(f'Spectral band {i+1}')
        axes[i].axis('off')  # Turn off axis
        
    plt.tight_layout()
    plt.show()

        
        
#%%
        
def plot_mask(mask):
    
    # Plot mask
    plt.imshow(mask)
    plt.title('Mask')
    
    # Add a colorbar legend
    cbar = plt.colorbar()
    cbar.set_label('Class')
    
    plt.show()
    
    