FROM base-image

RUN mkdir -p /eval_data

COPY eval_data/reference_gradcam.jpg /eval_data
COPY eval_data/reference_gradients.pt /eval_data
COPY eval_data/reference_activations.pt /eval_data
COPY eval_data/gradcam_explanation.txt /eval_data

RUN pip install torch