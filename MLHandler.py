import torch
import torch.nn as nn
from PIL import Image
from torchvision import models
import numpy as np
import consts


class MLHandler:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def get_pill_properties(image):
        image = MLHandler.prepare_image(image)
        color_model = MLHandler.get_color_model()
        shape_model = MLHandler.get_shape_model()

        return MLHandler.predict_properties(image, color_model, shape_model)

    @staticmethod
    def prepare_image(image):
        """
        prepares the image to be in the same manner as we trained the model:
        1 - crop it to be 150x150x3
        2 - normalize
        3 - view as batch x height x width x channel
        4 - move to cuda
        5 - set as float (each pixel int -> float)
        6 - permute to from NHWC to NCHW
        :param image: image to prepare
        :return: image ready for prediction
        """
        image = image.resize(consts.image_model_size, Image.ANTIALIAS)
        image = np.asarray(image)
        image = image.__truediv__(consts.image_max_value)
        image = torch.from_numpy(image)
        image = image.view(consts.image_view_as)
        image = image.cuda()
        image = image.float()
        image = image.permute(0, 3, 1, 2)
        return image

    @staticmethod
    def predict_properties(image, color_model, shape_model):
        color_prediction = color_model(image)
        shape_prediction = shape_model(image)
        _, predicted_color = torch.max(color_prediction.data, 1)
        _, predicted_shape = torch.max(shape_prediction.data, 1)

        return {consts.color_property: consts.color_classes[predicted_color.item()],
                consts.shape_property: consts.shape_classes[predicted_shape.item()]}

    @staticmethod
    def get_color_model():
        res_mod_color = models.resnet34(pretrained=True)
        num_ftrs = res_mod_color.fc.in_features
        res_mod_color.fc = nn.Linear(num_ftrs, len(consts.color_classes))
        res_mod_color = res_mod_color.to(MLHandler.device)
        res_mod_color.load_state_dict(torch.load(consts.color_model_path), strict=False)
        res_mod_color.eval()
        return res_mod_color

    @staticmethod
    def get_shape_model():
        res_mod_shape = models.resnet34(pretrained=True)
        num_ftrs = res_mod_shape.fc.in_features
        res_mod_shape.fc = nn.Linear(num_ftrs, len(consts.shape_classes))
        res_mod_shape = res_mod_shape.to(MLHandler.device)
        res_mod_shape.load_state_dict(torch.load(consts.shape_model_path), strict=False)
        res_mod_shape.eval()
        return res_mod_shape
