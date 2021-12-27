# DVR Blender Add-on Instructions
First, you can clone this repository to your locall machine using
```
git clone --recursive https://github.com/Creativity-AI-POC-PTL/DVR.git
```
Inside the `DVR` derectory, move `dvr_blender.py` into the `differentiable_volumetric_rendering` folder.

Then go to the `differentiable_volumetric_rendering` folder and follow the [installation](https://github.com/autonomousvision/differentiable_volumetric_rendering#installation) instructions to set up.

Suppose your absolute path to the `differentiable_volumetric_rendering` folder is `<some path>/differentiable_volumetric_rendering/`. Edit some lines of code to ensure Blender can find the correct paths:
1. In `dvr_blender.py`, replace line 17 with your absolute path.
2. In `generate.py`, add the following code after line 43:
    ```python
    abs_path = "<some path>/differentiable_volumetric_rendering/" # replace your path here
    if not generation_dir.startswith(abs_path):
        generation_dir = abs_path + generation_dir
    ```
    After editing, the code should look like this:

    <img width="559" alt="image" src="https://user-images.githubusercontent.com/93342727/147511784-0a3dd195-366a-4a91-975b-6d47d59cfad3.png">
3. In `im2mesh/checkpoints.py`, add the following code after line 18:
    ```python
    abs_path = "<some path>/differentiable_volumetric_rendering/" # replace your path here
    if not checkpoint_dir.startswith(abs_path):
        checkpoint_dir = abs_path + checkpoint_dir
    ```
4. In `im2mesh/config.py`, add the following coder after line 23:
    ```
    abs_path = "C:/Users/Local_Admin/3D_Gen/differentiable_volumetric_rendering/"
    if not path.startswith(abs_path):
        path = abs_path + path
    if default_path is not None and not default_path.startswith(abs_path):
        default_path = abs_path + default_path
    ``` 
    
Now you are ready to install DVR in Blender. Open Blender and go to `Edit -> Preferences -> Add-ons`.

<img width="692" alt="image" src="https://user-images.githubusercontent.com/93342727/147512848-474d705b-90d2-4a1e-89e1-cb8d5a1a5230.png">

Then press the `Install` botton and browse to and select `dvr_blender.py`. After installation, make sure the DVR add-on is checked.

<img width="498" alt="image" src="https://user-images.githubusercontent.com/93342727/147513068-d6c0d257-cb7a-49da-8763-0f62a3b3753b.png">

Next you can run DVR directly in Blender. Go to `Add -> Run DVR`, and then select the folder containing the input images.

<img width="365" alt="image" src="https://user-images.githubusercontent.com/93342727/147513254-cfd3fa3f-8389-4ca4-be8d-22a804a19759.png">

For example, you can select the `differentiable_volumetric_rendering/media/demo/choy_renderings` folder. Make sure that you are selecting a folder instead of a file.

<img width="674" alt="image" src="https://user-images.githubusercontent.com/93342727/147513360-a4e47341-6dd3-486c-a0ef-e7df1475ec29.png">

After it finishes, select `Vertx` to view the vertex colors.

<img width="549" alt="image" src="https://user-images.githubusercontent.com/93342727/147513622-ed0b83f5-95bf-4fac-9090-a471bbfff5f7.png">

