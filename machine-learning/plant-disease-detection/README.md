## Directory contents 📂

| Content | Description   |
| :--- | :--- |
| [analysis.ipynb](./src/analysis.ipynb)  | Jupyter Notebook containing Python code and visualizations  |
| [analysis.html](https://antonio-cln.github.io/data-science-portfolio/machine-learning/plant-disease-detection/src/analysis.html)  | HTML rendered version of the analysis |
| [technical-presentation.pdf](./technical-presentation.pdf) | Technical presentation of the findings |

## Analysis Overview 
The goal of this analysis is to make us of the PlantDoc dataset, implement machine learning models and compare them in order to identify a possible good solution to detect plant disease presence.  


#### Data Exploration & Feature Engineering
Extracted image metadata (dimensions, aspect ratio, intensity, channels) reveals class imbalance (4:1 ratio) and structural zeros explained by the Disease Triangle. Data preprocessing involved standardizing images to RGB, cropping aspect ratios near 1, and accounting for dual-peak pixel intensity variations.

#### Embeddings Extraction & Dimensionality Reduction
Features were extracted using pre-trained ResNet-50 (2,048 dimensions) and Google ViT Base Patch16-224 (768 dimensions). PCA reduced redundancy (to 500 and 200 dimensions, keeping >80% variance), while t-SNE and UMAP (tuned via Optuna) enabled 2D/3D visualizations.

#### Unsupervised Clustering Analysis
Evaluated spatial grouping using DBSCAN, HDBSCAN, and Mahalanobis K-Means. Metrics like DBCV, Silhouette Score, and ARI showed that Mahalanobis K-Means and HDBSCAN better handle varying cluster densities and separate complex feature structures.

#### Model Fine-Tuning & Explainable AI (XAI)
Models were fine-tuned using domain-safe data augmentation (rotations and mirroring without altering colors or ratios). Saliency Maps and Grad-CAM/ViT Rollout provided visual transparency into regions driving model decisions.

#### Classification & Performance Comparison
Evaluated via macro/weighted F1-scores to handle class imbalance, Google ViT outperformed ResNet-50, achieving higher overall classification accuracy (ViT weighted F1-score: 0.77 vs ResNet-50: 0.66)

#### Conclusions
Fine-tuning noticeably improved low-dimensional class separation for both models, with ViT proving superior for image classification. Remaining misclassification challenges mainly involve closely related species from the same plant family (e.g., Tomatoes and Potatoes).
