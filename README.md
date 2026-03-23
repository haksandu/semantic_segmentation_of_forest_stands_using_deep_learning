# Semantic segmentation of forest stands using deep learning

This repository is mainly published for **documentation and transparency** purposes to support the methodology and findings in the associated research article. It provides the full code and logic used for the semantic segmentation of forest stands.

The authors do not own the input data and cannot share it. However, the trained model is available for download through: [https://huggingface.co/haksandu/stand_delineation_model/tree/main](https://huggingface.co/haksandu/stand_delineation_model/tree/main). The model uses a 5-channel input (RGB, Near-Infrared, and Canopy Height Model) at a 1m resolution. To apply the model, follow the preprocessing steps in the R scripts (found in `scripts/create_image_tiles/`) and use the code in the **"Test time prediction"** section of the Jupyter notebook as explained below.

Detailed methodology and analysis can be found in the associated publication:

> **Article Title:** Semantic segmentation of forest stands using deep learning  
> **DOI:** [https://doi.org/10.14214/sf.25010](https://doi.org/10.14214/sf.25010)

---

## 📂 Repository Structure

The project is organized to flow from raw data preprocessing (R) to model training and inference (Python).

*   **`data/`**: (Empty) Storage for image tiles and masks.
*   **`environments/`**: Contains `environment.yml` to recreate the required software environment.
*   **`envs/`**: (Empty) Default location for the active environment.
*   **`model/`**: (Empty) **Action Required:** Download the model weights from [Link to HuggingFace] and place them here.
*   **`scripts/`**:
    *   **`create_image_tiles/`**: R scripts (numbered 01–06) for data generation and canopy rasterization (via `lidR`).
    *   **`imageutils/`**: Python helper scripts for the main pipeline.
    *   **`loss_function.py` & `metric.py`**: Custom training logic including MCC metrics.
    *   **`main.ipynb`**: The primary notebook for data loading, augmentations, training (Optuna/WandB), and testing.

---

## ⚙️ Setup and Requirements

### 1. Working Directory
**Important:** The root folder of this repository must be set as the working directory. All scripts use relative paths (e.g., `data/` or `model/`) starting from this base location.

### 2. Environment
To recreate the environment used for this project:
1. Open a terminal in the project root.
2. Run: `conda env create --prefix ./envs/segmentation_of_forest_stands --file ./environments/segmentation_of_forest_stands.yml`
3. Activate the environment: `conda activate ./envs/segmentation_of_forest_stands`

---

## 🌲🛰️ Data & Model Specifications

The model was trained using image tiles of 512x512 pixels at 1x1m resolution with the following configuration:

*   **Input Channels:** 5 Channels — Red, Green, Blue, Near-Infrared (I), and Canopy Height Model (CHM).
*   **Data Format:** Input tensors are loaded as `(#Images, Height, Width, 5)`.
*   **Normalization:** All input values are normalized to the `[0, 1]` range.
*   **Augmentations:** Training includes random horizontal flips and brightness/contrast adjustments.
*   **Output Classes:** One-hot encoded (5 classes):
    *   **NF** - Non-Forested areas
    *   **I-II** - Clearcuts/Regeneration
    *   **III** - Young thinning stage forest
    *   **IV** - Old thinning stage forest
    *   **V** - Mature forest ready for harvest

---

## 🚀 How to Use

### Preprocessing (R)
Run the scripts in `scripts/create_image_tiles/` in numerical order. 
*   **Note:** You must manually check and update the input file paths in the first few scripts to match your local data source. 
*   If the paths are set correctly, the scripts will automatically output the processed tiles into the `data/` folder.

### Training and Inference (Python)
1. Download the trained model from: **[Link to Model]**.
2. Save the model in the `model/` folder.
3. Open `scripts/main.ipynb`.
4. The notebook contains the full pipeline for loading data, running the training loop (via Optuna and WandB), and applying the model to test data.
5. To test the model on your own data, refer to the **"Test time prediction"** block at the end of the notebook.

---

## 📄 License and Usage
The code is provided for documentation purposes to support the findings in the linked article. The raw training data is not owned by the authors, and we do not have the right to share the data publicly.