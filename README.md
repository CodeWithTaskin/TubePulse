# TubePluse - YouTube Comment Sentiment Analyzer

<div align="center">
  <img src="https://github.com/CodeWithTaskin/TubePulse/blob/main/plugin/icons/icon128.png?raw=true" alt="TubePluse Banner">
  
  [![Firefox Addons](https://img.shields.io/badge/Firefox_Addons-FF7139?logo=firefoxbrowser&logoColor=white)](https://addons.mozilla.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)
  [![Azure](https://img.shields.io/badge/Azure-0089D6?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
</div>

## 🌟 Transform YouTube Comments into Actionable Insights

TubePluse is a cutting-edge browser extension that analyzes sentiment in YouTube comments using advanced machine learning. Gain instant insights into audience reactions through beautiful visualizations and data-driven metrics.

```mermaid
graph TD
    A[Browser Extension] -->|Fetch Comments| B(YouTube API)
    A -->|Send Data| C[Flask API]
    C -->|Data Processing| D[Data Pipeline]
    subgraph Azure Cloud
        C -->|Hosted on| E[Azure VM]
        F[Azure Container Registry] -->|Deploy| E
    end
    subgraph Data Pipeline
        D1[Data Ingestion] -->|MongoDB Atlas| D
        D --> D2[Data Validation]
        D2 --> D3[Data Transformation]
        D3 --> D4[Model Training]
        D4 --> D5[Model Evaluation]
        D5 -->|Register Model| G[Dagshub Registry]
    end
    H[GitHub Actions] -->|CI/CD| F
    G -->|Load Model| C
    C -->|Return Analysis| A
    A -->|Visualize| I[User Dashboard]
    
    classDef azure fill:#0089D6,color:white;
    classDef pipeline fill:#4cc9f0,color:black;
    classDef registry fill:#1a1a2e,color:white;
    classDef external fill:#47A248,color:white;
    
    class E,F azure;
    class D1,D2,D3,D4,D5 pipeline;
    class G registry;
    class B,H external;
```
## 🎥 Demo Video
https://github.com/user-attachments/assets/da273429-f3af-4f8b-bc7f-a5f74b0a7566 


## ✨ Key Features

| Feature | Description | Visualization |
|---------|-------------|--------------|
| **Sentiment Analysis** | Real-time classification of comments into Positive/Negative/Neutral | <img src="https://via.placeholder.com/300x150/0f3460/ffffff?text=Pie+Chart" width="200"> |
| **Word Cloud** | Visual representation of most frequent words | <img src="https://via.placeholder.com/300x150/0f3460/ffffff?text=Word+Cloud" width="200"> |
| **Top Comments** | Curated list of most impactful comments | <img src="https://via.placeholder.com/300x150/0f3460/ffffff?text=Top+Comments" width="200"> |
| **Automated Pipeline** | End-to-end MLOps workflow | <img src="https://via.placeholder.com/300x150/0f3460/ffffff?text=MLOps" width="200"> |

## 🚀 How It Works

### System Architecture

```mermaid
graph TD
    A[Browser Extension] -->|Fetch Comments| B(YouTube API)
    A -->|Send Data| C[Flask API]
    C --> D[Data Pipeline]
    subgraph Data Pipeline
        D1[Data Ingestion] --> D2[Data Validation]
        D2 --> D3[Data Transformation]
        D3 --> D4[Model Builder]
        D4 --> D5[Model Pusher]
    end
    D --> E[MongoDB Atlas]
    D --> F[MLflow]
    D --> G[Dagshub]
    C -->|Deploy| H[Azure VM]
    I[GitHub Actions] -->|CI/CD| H
```

### Workflow Overview

1. **User activates extension** on YouTube video page
2. **Comments fetched** (up to 1000 comments)
3. **Data sent to backend** for processing
4. **ML pipeline executes**:
   - Data validation and transformation
   - Model training and evaluation
   - Model registration in Dagshub
5. **Results returned** to extension
6. **Interactive dashboard displayed** with visualizations

## 🛠️ Technical Implementation

### Automated ML Pipeline

```mermaid
graph LR
    A[MongoDB Atlas] --> B[Data Ingestion]
    B --> C[Data Validation]
    C -->|Validation Report| D{Report Valid?}
    D -->|Yes| E[Data Transformation]
    D -->|No| F[Error Handling]
    E --> G[Model Training]
    G --> H[Model Evaluation]
    H --> I{Improved Performance?}
    I -->|Yes| J[Register in Model Registry]
    I -->|No| K[Keep Previous Model]
    J --> L[Deploy to Production]
```

### Technology Stack

**Core Components**  
<div>
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Scikit_learn-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn">
</div>

**MLOps Infrastructure**  
<div>
  <img src="https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white" alt="MLflow">
  <img src="https://img.shields.io/badge/Dagshub-000000?logo=dagshub&logoColor=white" alt="Dagshub">
</div>

**Cloud Deployment**  
<div>
  <img src="https://img.shields.io/badge/Azure-0089D6?logo=microsoftazure&logoColor=white" alt="Azure">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions">
</div>

## 🧩 Installation & Setup

### Browser Extension
Available on Firefox Addons Marketplace:  
[![Get TubePluse on Firefox](https://via.placeholder.com/200x60/FF7139/ffffff?text=Download+for+Firefox)](https://addons.mozilla.org/)

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/tubepluse.git
cd tubepluse

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
cd backend
python app.py

# Load extension in browser
1. Enable developer mode in browser
2. Load unpacked extension from /extension directory
```

## 🔄 CI/CD Pipeline

```mermaid
graph TB
    A[Code Commit] --> B[GitHub Actions]
    B --> C[Build Docker Image]
    C --> D[Run Unit Tests]
    D --> E[Push to Azure Container Registry]
    E --> F[Deploy to Azure VM]
    F --> G[Run Integration Tests]
    G --> H[Send Deployment Notification]
```

## 📊 Results Visualization

<div align="center">
  <img src="https://via.placeholder.com/400x300/1a1a2e/ffffff?text=Sentiment+Pie+Chart" alt="Pie Chart" width="30%">
  <img src="https://via.placeholder.com/400x300/16213e/ffffff?text=Comment+Word+Cloud" alt="Word Cloud" width="30%">
  <img src="https://via.placeholder.com/400x300/0f3460/ffffff?text=Top+Comments" alt="Top Comments" width="30%">
</div>

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Project Lead: [Your Name](mailto:your.email@example.com)  
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/tubepluse)](https://github.com/yourusername/tubepluse/issues)

