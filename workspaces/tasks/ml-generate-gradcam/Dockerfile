FROM ghcr.io/li-boxuan/task-base-image:1.0.0

COPY eval_data/reference_gradcam.jpg /utils
COPY eval_data/reference_gradients.pt /utils
COPY eval_data/reference_activations.pt /utils

RUN pip install torch==2.5.1