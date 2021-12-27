# DVR Blender Add-on Instructions
First, you can clone this repository to your locall machine using
```
git clone --recursive https://github.com/Creativity-AI-POC-PTL/DVR.git
```
Inside the `DVR` derectory, move `dvr_blender.py` into the `differentiable_volumetric_rendering` folder.

Then go to the `differentiable_volumetric_rendering` folder and follow the [installation](https://github.com/autonomousvision/differentiable_volumetric_rendering#installation) instructions to set up.

Suppose your absolute path to the `differentiable_volumetric_rendering` folder is `<some path>/differentiable_volumetric_rendering/`. Edit some lines of code to ensure Blender can find the correct paths:
1. In `generate.py`, add the following code after line 43:
    ```python
    abs_path = "<some path>/differentiable_volumetric_rendering/" # replace your path here
    if not generation_dir.startswith(abs_path):
        generation_dir = abs_path + generation_dir
    ```
    After editing, the code should look like this:

    <img width="559" alt="image" src="https://user-images.githubusercontent.com/93342727/147511784-0a3dd195-366a-4a91-975b-6d47d59cfad3.png">
2. In `im2mesh/checkpoints.py`, add the following code after line 18:
    ```python
    abs_path = "<some path>/differentiable_volumetric_rendering/" # replace your path here
    if not checkpoint_dir.startswith(abs_path):
        checkpoint_dir = abs_path + checkpoint_dir
    ```
3. In `im2mesh/config.py`, add the following coder after line 23:
    ```
    abs_path = "C:/Users/Local_Admin/3D_Gen/differentiable_volumetric_rendering/"
    if not path.startswith(abs_path):
        path = abs_path + path
    if default_path is not None and not default_path.startswith(abs_path):
        default_path = abs_path + default_path
    ```

  
