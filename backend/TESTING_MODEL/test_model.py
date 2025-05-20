from tensorflow.keras.models import load_model

# Correct path to your model
model_path = "C:/Users/LEGION/OneDrive/Desktop/backend/models/fusion_model.h5"

# Load the model
model = load_model(model_path)

# Print model architecture summary
model.summary()