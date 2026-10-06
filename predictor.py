import torch
from torchvision import models, transforms
from PIL import Image
import io

class WasteClassifier:
    def __init__(self):
        self.model_name = "EfficientNet-B0"
        self.categories = ['Plastic', 'Paper', 'Cardboard', 'Glass', 'Metal', 'Organic', 'E-Waste', 'Mixed Waste', 'Unknown']
        # Note: Using uninitialized weights for speed/demo purposes if you haven't trained it yet.
        self.model = models.efficientnet_b0(pretrained=False) 
        self.model.classifier[1] = torch.nn.Linear(1280, len(self.categories))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])

    def predict(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            tensor = self.transform(image).unsqueeze(0)

            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                confidence, predicted_idx = torch.max(probabilities, 0)
            
            conf_val = round(confidence.item(), 4)
            pred_class = self.categories[predicted_idx.item()]
            if conf_val < 0.60: pred_class = "Unknown"

            return {"predicted_class": pred_class, "confidence": conf_val, "model_name": self.model_name}
        except Exception as e:
            return {"predicted_class": "Unknown", "confidence": 0.0, "error": str(e), "model_name": self.model_name}

classifier = WasteClassifier()
