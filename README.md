#Overview
Any iterable object

- Able to handle batches, multiple images and single image.
- Able to perform augmentations based on specific image.
- Consists of 3 compoents - input_dataflow, augment_pipeline, output_dataflow. Easy to build an augmentor on any datasets.
- Handle with X and y.
- Able to perform augmentations on specific channel

# Documentation




# Examples
## Easy Way
Feel free to use temporary instance, instances with same parameters are cached and only be created once.
```python
from MessUp import *
img = Dislocate((2,10))(img)
```
## Simple

## Use Wrapper
Use wrapper to create complicated and customed operations
```python
aug = WithChannels((0,1))(Blur(3))
img_aug = aug(img)
```

## Write an Operation
All you need is to:
1. write a class from Operation
2. define all parameters
3. write a function to handle single image.
```python
class Custom(Operation):
    _fields = ['parameter1', 'parameter2']
    def perform_on_image(self, img):
        # write your code here
        return res
```


## Digital Docs to Natural Scenes

