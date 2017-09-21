# Overview
Any iterable object

- Able to handle batches, multiple images and single image.
- Able to perform augmentations based on specific image.
- Consists of 3 compoents - input_dataflow, augment_pipeline, output_dataflow. Easy to build an augmentor on any datasets.
- Handle with X and y.
- Able to perform augmentations on specific channel

# Documentation




# Examples
## Simple

```python
from augmentor.operations import *
from augmentor.pipeline import Pipeline

p = Pipeline()
p.add()
p.sequential(
    [

    ],
    True
)
p.add()
print(p)
'''Output:


'''
```
## Digital Docs to Natural Scenes
