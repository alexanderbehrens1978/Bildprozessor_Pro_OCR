from PIL import ImageTk
from modules.filters import apply_filter

def update_image_op(app_instance, *args):
    if app_instance.original_image:
        img = app_instance.original_image.copy()
        for enabled_var, filter_var, strength_var in app_instance.layer_vars:
            if enabled_var.get():
                img = apply_filter(img, filter_var.get(), strength_var.get())
        app_instance.processed_image = img
        show_image_op(img, app_instance.right_canvas)

def show_image_op(image, canvas):
    canvas.delete("all")
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(10, 10, image=photo, anchor="nw")
    canvas.image = photo
    width, height = image.size
    canvas.config(scrollregion=(0, 0, width + 20, height + 20))

def apply_filter_op(img, filter_name, strength=1.0):
    return apply_filter(img, filter_name, strength)
