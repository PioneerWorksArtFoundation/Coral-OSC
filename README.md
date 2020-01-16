# OSC Communication via Coral Dev Board

At the Pioneer Works Tech Lab, we are experimenting with approaches for using OSC to communicate over the network between small, on-device ML products and other computers running programs that support OSC. Specifically, we are using the [Coral Dev Board](https://coral.ai/products/dev-board/), a small board which uses Google's EdgeTPU harderware to support on-device machine learning inferrence and is ideal for IoT use cases.

We're experimenting with the following workflow:

1. Train a simple computer vision model using [Teachable Machine](https://teachablemachine.withgoogle.com/).
2. Export the model and Python code for Tensorflow Lite on EdgeTPU.
3. Load the model and onto the Coral Dev Board.
4. Retrofit the Python code from Teachable Machine with changes to send messages via OSC.
5. Run an OSC server on a separate device that will receive OSC messages from the code running on the Coral Dev Board.

This repository includes setup instructions and example code for experimenting with this workflow.

### Setup the Coral Dev Board

You can skip this step if you're working with a Coral Dev Board that someone has already set up. Detailed instructions on setting up a new Coral Dev Board can be found here:

[Get started with the Dev Board](https://coral.ai/docs/dev-board/get-started/) by Coral.ai.

From personal experience, I experienced some challenges with the following:

- **Installing the [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) by Silicon Labs** for Mac: Installing these drivers required multiple attempts and a few restarts to my computer. Here are a few forum threads with possible steps for debugging [1](https://www.silabs.com/community/interface/forum.topic.html/cp210x_usb_to_uartb-LJMf), [2](https://www.silabs.com/community/interface/knowledge-base.topic.10.10.html/usb_to_uart_bridgev-Dnef), [3](https://community.wia.io/d/2-how-to-install-usb-to-uart-bridge-vcp-drivers-on-mac-os-x).
- Using `screen` to access the board with `screen /dev/cu.SLAB_USBtoUART 115200`:
  - You can use `ls /dev/cu.*` to check to see if the SLAB_USBtoUART device file is present.
  - Use `kextstat | grep silabs` to see if the SiLabs kernel extension is enabled.

Try running some of the example code suggested in the Getting Started instructions to verify that your setup is working.

### Training a Model with Teachable Machine

For this particular experiment, we are using [Teachable Machine](https://github.com/googlecreativelab/teachablemachine-community/blob/master/snippets/markdown/image/edgetpu/python.md) to train simple computer vision models that we can run on the Coral Dev Board. You can follow the instructions on that site to create a simple model.

Once it's done, export the model for EdgeTPU. Download the model files (a .tflite file and a .txt file). The export dialog will show [this exemplary code snippet](https://github.com/googlecreativelab/teachablemachine-community/blob/master/snippets/markdown/image/edgetpu/python.md), but you can instead use the code in this repository. See the section on running example code below.

### Running a Custom Model on the Coral Dev Board

Next, we need to copy our model files from our local computer onto the Coral Dev Board. If you followed the approach suggested in [Coral's Getting Started guide](https://coral.ai/docs/dev-board/get-started/#2-connect-to-the-boards-shell-via-mdt), you should have the `mdt` command installed. If so, the easiest method would be to use `mdt push your-file.txt` to transport a local file on your computer to the Coral Dev Board over SSH. Alternatively, if you're not using `mdt`, you should be able to move the files using the [standard `scp` command](https://www.ssh.com/ssh/scp).
