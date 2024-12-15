# PyThumbPad

[![PyPI version](https://badge.fury.io/py/py-thumbpad.svg?version=latest)](https://badge.fury.io/py/py-thumbpad)

PyThumbPad is a customizable virtual thumb pad for directional input, designed for use in Pygame projects. It features a central donut-shaped control area and a movable button pad, making it ideal for mobile games or any application requiring a thumb stick-style input.

## Features

- **Customizable Appearance**: Easily change colors and sizes for the donut and button pad.
- **Directional Input**: Supports 4 or 8 directional quadrants for precise input.
- **Simple Integration**: Easy to add to any Pygame project with minimal setup.
- **Responsive Input Handling**: Smoothly tracks user input and updates the direction accordingly.

## Installation using PyPI

You can install the `py_thumbpad` package directly from PyPI using pip:

```bash
pip install py_thumbpad
```

## Installation using GIT

Clone the repository and include the `py_thumbpad` package in your Pygame project.

```bash
git clone https://github.com/kerodekroma/py-thumbpad.git
```

## Updating the PyThumbPad Package

If you've already installed the `py_thumbpad` package and want to update it to the latest version, you can easily do so using `pip`. Run the following command in your terminal or command prompt:

```bash
pip install --upgrade py_thumbpad
```

## Usage
Here's a basic example of how to use PyThumbPad in your Pygame project:

```py
from py_thumbpad import PyThumbPad, PY_THUMBPAD_Directions

# Initialize the thumbpad at position (400, 300)
thumbpad = PyThumbPad((400, 300), {})

# In your game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        thumbpad.listen_events(event)
    
    # Check the direction the thumbpad is pointing to
    if PY_THUMBPAD_Directions.TOP in thumbpad.directions:
        print("Moving UP!")
    elif PY_THUMBPAD_Directions.BOTTOM in thumbpad.directions:
        print("Moving DOWN!")
    elif PY_THUMBPAD_Directions.LEFT in thumbpad.directions:
        print("Moving LEFT!")
    elif PY_THUMBPAD_Directions.RIGHT in thumbpad.directions:
        print("Moving RIGHT!")
    
    # Update and render the thumbpad
    thumbpad.update()
    thumbpad.render(screen)
    
    pygame.display.flip()

pygame.quit()
```

## Options

When initializing PyThumbPad, you can pass a dictionary of options to customize the appearance and behavior:

- `quadrants`: The number of directional quadrants (4 for up, down, left, right; 8 for diagonals as well). Default is 4.

- `donut_color`: The color of the donut-shaped pad. Default is (123, 157, 243).

- `button_color`: The color of the movable button pad. Default is (255, 255, 0).

- `donut_bg_color`: The background color of the donut. Default is (0, 0, 0).

Example:

```py
thumb_pad = PyThumbPad((400, 300), {
    "quadrants": 8,
    "donut_color": (200, 100, 100),
    "button_color": (100, 200, 100),
    "donut_bg_color": (50, 50, 50)
})
```

## Methods

`update()`
Updates the state of the button pad. This method should be called within the game loop.

`render(screen)`
Renders the thumb pad on the provided Pygame surface.

`listen_events(event)`
Handles Pygame input events and updates the thumb pad's state.

`get_directions(current_angle)`
Returns the direction based on the current angle and the number of quadrants. This method is used internally by listen_events.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss any changes or improvements.

## License
This project is licensed under the MIT License - see the MIT-LICENSE.txt file for details.

