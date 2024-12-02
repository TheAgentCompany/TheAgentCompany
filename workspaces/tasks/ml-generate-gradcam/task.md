We are trying to understand why Computer Vision models make the decisions they do. To do this, we are generating GradCAM explanations for images. You will first need to load a pre-train resnet18 model. You will need to download an image 'test_image.jpg' and then generate a GradCAM image for it and save it as 'gradcam_output.jpg' in the workspace directory. You will need to analyse the GradCAM image and write a short explanation (preferably 1 sentence) of what the predicted class is and why the model predicted it. Save the explanation in 'gradcam_explanation.txt' file in the workspace directory. You should also save the gradients and activations as 'raw_gradients.pt' and 'raw_activations.pt' respectively. remember this is with respect to the last Convolutional layer.

In order to maintain the dimensionality standards, load the image as follows:

```python
transforms.Resize(256),
transforms.CenterCrop(224),
transforms.ToTensor(),
transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
```

Use the cv2.COLORMAP_JET colormap to generate the heatmap and multiply it by 0.4 before superimposing it on the original image.

OwnCloud can be accessed at: http://the-agent-company.com:8092
