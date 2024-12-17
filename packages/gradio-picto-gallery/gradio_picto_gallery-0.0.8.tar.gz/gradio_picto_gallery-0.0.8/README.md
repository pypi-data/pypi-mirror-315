---
tags: [gradio-custom-component, Gallery]
title: gradio_picto_gallery
short_description: gallery with download button and like/dislike
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_picto_gallery`
<a href="https://pypi.org/project/gradio_picto_gallery/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_picto_gallery"></a>  

gallery for the picto app

## Installation

```bash
pip install gradio_picto_gallery
```

## Usage

```python
import gradio as gr
from gradio_picto_gallery import PictoGallery

example = PictoGallery().example_value()
payload = PictoGallery().example_payload()

with gr.Blocks() as demo:
    with gr.Row():
        gallery = PictoGallery(
            value=example,
            height=1000,
            min_width=500,
            object_fit="scale_down",
            interactive=False,
            hide_close_button=True,
        )  #

    def on_toggle_favorite(value, evt: gr.EventData):
        favorite = evt._data["favorite"]
        if favorite:
            # add here logic to save the image to favorites
            print(f"Add {evt._data['image']['orig_name']} to favorites")
        else:
            # add here logic to remove the image from favorites
            print(f"Remove {evt._data['image']['orig_name']} from favorites")

    def on_like(evt: gr.EventData):
        print(f"Like {evt._data['image']['orig_name']}")

    def on_dislike(evt: gr.EventData):
        print(f"Dislike {evt._data['image']['orig_name']}")

    def on_edit(evt: gr.EventData):
        print(f"Edit {evt._data['image']['orig_name']}")

    gallery.toggle_favorite(on_toggle_favorite, gallery, None)
    gallery.like(on_like, None, None)
    gallery.dislike(on_dislike, None, None)
    gallery.edit(on_edit, None, None)


if __name__ == "__main__":
    demo.launch()

```

## `PictoGallery`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
Sequence[
        np.ndarray | PIL.Image.Image | str | Path | tuple
    ]
    | Callable
    | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">List of images to display in the gallery by default. If callable, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>format</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"webp"</code></td>
<td align="left">Format to save images before they are returned to the frontend, such as 'jpeg' or 'png'. This parameter only applies to images that are returned from the prediction function as numpy arrays or PIL Images. The format should be supported by the PIL library.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>show_like_dislike</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will show like and dislike buttons for each image in the gallery. Default is True.</td>
</tr>

<tr>
<td align="left"><code>show_edit_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will show an edit button for each image in the gallery. Default is True.</td>
</tr>

<tr>
<td align="left"><code>hide_close_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, will hide the close button in the top right corner of the gallery. Default is False.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>

<tr>
<td align="left"><code>columns</code></td>
<td align="left" style="width: 25%;">

```python
int | list[int] | Tuple[int, ...] | None
```

</td>
<td align="left"><code>2</code></td>
<td align="left">Represents the number of images that should be shown in one row, for each of the six standard screen sizes (<576px, <768px, <992px, <1200px, <1400px, >1400px). If fewer than 6 are given then the last will be used for all subsequent breakpoints</td>
</tr>

<tr>
<td align="left"><code>rows</code></td>
<td align="left" style="width: 25%;">

```python
int | list[int] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Represents the number of rows in the image grid, for each of the six standard screen sizes (<576px, <768px, <992px, <1200px, <1400px, >1400px). If fewer than 6 are given then the last will be used for all subsequent breakpoints</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | float | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The height of the gallery component, specified in pixels if a number is passed, or in CSS units if a string is passed. If more images are displayed than can fit in the height, a scrollbar will appear.</td>
</tr>

<tr>
<td align="left"><code>allow_preview</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, images in the gallery will be enlarged when they are clicked. Default is True.</td>
</tr>

<tr>
<td align="left"><code>preview</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, downloadGallery will start in preview mode, which shows all of the images as thumbnails and allows the user to click on them to view them in full size. Only works if allow_preview is True.</td>
</tr>

<tr>
<td align="left"><code>selected_index</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The index of the image that should be initially selected. If None, no image will be selected at start. If provided, will set downloadGallery to preview mode unless allow_preview is set to False.</td>
</tr>

<tr>
<td align="left"><code>object_fit</code></td>
<td align="left" style="width: 25%;">

```python
Literal[
        "contain", "cover", "fill", "none", "scale-down"
    ]
    | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">CSS object-fit property for the thumbnail images in the gallery. Can be "contain", "cover", "fill", "none", or "scale-down".</td>
</tr>

<tr>
<td align="left"><code>show_share_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.</td>
</tr>

<tr>
<td align="left"><code>show_download_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will show a download button in the corner of the selected image. If False, the icon does not appear. Default is True.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, the gallery will be interactive, allowing the user to upload images. If False, the gallery will be static. Default is True.</td>
</tr>

<tr>
<td align="left"><code>type</code></td>
<td align="left" style="width: 25%;">

```python
Literal["numpy", "pil", "filepath"]
```

</td>
<td align="left"><code>"filepath"</code></td>
<td align="left">The format the image is converted to before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. If the image is SVG, the `type` is ignored and the filepath of the SVG is returned.</td>
</tr>

<tr>
<td align="left"><code>show_fullscreen_button</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will show a fullscreen icon in the corner of the component that allows user to view the gallery in fullscreen mode. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `select` | Event listener for when the user selects or deselects the PictoGallery. Uses event data gradio.SelectData to carry `value` referring to the label of the PictoGallery, and `selected` to refer to state of the PictoGallery. See EventData documentation on how to use this event data |
| `upload` | This listener is triggered when the user uploads a file into the PictoGallery. |
| `change` | Triggered when the value of the PictoGallery changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `toggle_favorite` | Triggered when the user clicks on the favorite icon of an image |
| `like` | Triggered when the user clicks on the like button of an image |
| `dislike` | Triggered when the user clicks on the dislike button of an image |
| `edit` | Triggered when the user clicks on the edit button of an image |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the list of images as a list of (image, caption) tuples, or a list of (image, None) tuples if no captions are provided (which is usually the case). The image can be a `str` file path, a `numpy` array, or a `PIL.Image` object depending on `type`.
- **As input:** Should return, expects the function to return a `list` of images, or `list` of (image, `str` caption) tuples. Each image can be a `str` file path, a `numpy` array, or a `PIL.Image` object.

 ```python
 def predict(
     value: list[tuple[str, str | None, bool | None]]
    | list[tuple[PIL.Image.Image, str | None, bool | None]]
    | list[tuple[numpy.ndarray, str | None, bool | None]]
    | None
 ) -> list[
        numpy.ndarray
        | PIL.Image.Image
        | pathlib.Path
        | str
        | tuple[
            numpy.ndarray
            | PIL.Image.Image
            | pathlib.Path
            | str,
            str,
        ]
        | tuple[
            numpy.ndarray
            | PIL.Image.Image
            | pathlib.Path
            | str,
            str,
            bool,
        ]
    ]
    | None:
     return value
 ```
 
