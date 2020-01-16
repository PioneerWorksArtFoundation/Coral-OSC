# OSC Communication via Coral Dev Board

At the Pioneer Works Tech Lab, we are experimenting with approaches for using OSC to communicate over the network between small, on-device ML products and other computers running programs that support OSC. Specifically, we are using the [Coral Dev Board](https://coral.ai/products/dev-board/), a small board which uses Google's EdgeTPU harderware to support on-device machine learning inferrence and is ideal for IoT use cases.

We're experimenting with the following workflow:

1. Train a simple computer vision model using [Teachable Machine](https://teachablemachine.withgoogle.com/);
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
