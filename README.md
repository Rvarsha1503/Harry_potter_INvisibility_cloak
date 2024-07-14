# Harry_potter_Invisibility_cloak
This project brings the magic of Harry Potter's invisibility cloak to life using computer vision techniques with OpenCV. By using a blue cloth as the cloak, the program captures the background and then replaces the blue areas of the frame with the captured background, making the person wearing the cloak appear invisible.
# Harry Potter Invisibility Cloak

This project simulates the invisibility cloak effect from the Harry Potter series using OpenCV. By using a blue cloth, the program replaces the cloth with the background, making the person wearing it appear invisible.

## Requirements

- Python 3.x
- OpenCV
- NumPy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/invisibility-cloak.git
    cd invisibility-cloak
    ```

2. Install the required packages:
    ```bash
    pip install opencv-python numpy
    ```

## Usage

1. Run the script:
    ```bash
    python invisibility_cloak.py
    ```

2. Instructions:
    - Ensure the blue cloth is not in the frame when the program starts, as it captures the background initially.
    - Once the background is captured, the program will start detecting the blue cloth and replace it with the background, creating the invisibility effect.
    - Press `q` to quit the program.

## Code Explanation

### capture_background(cap, num_frames=60)
Captures the background by taking multiple frames and averaging them to get a stable background image.

### refine_mask(mask)
Refines the mask by applying morphological operations to remove noise and fill gaps.

### main()
The main function that:
1. Captures the background.
2. Continuously reads frames from the webcam.
3. Detects the blue cloth and replaces it with the background.
4. Displays the final output.

## Troubleshooting

- **Blue cloth not detected properly:** Adjust the `lower_blue` and `upper_blue` values in the `main()` function to match the specific shade of blue.
- **Background mismatch:** Ensure the background is static and the lighting conditions are consistent.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.

## License

This project is licensed under the MIT License.

