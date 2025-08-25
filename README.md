\# 🧠 AI-Powered Dataset Annotator with Active Learning



This project is an advanced web application designed to accelerate the annotation process for image datasets. By combining Large Multimodal Models (LMMs) and Active Learning techniques, this tool automatically generates initial "weak labels" and then intelligently prioritizes the most uncertain samples for human review. It offers a practical solution to one of the biggest bottlenecks in the AI industry: the time and cost of data labeling.



---



\### 📸 Live Demo



\[Insert a cool GIF or screenshot of the Streamlit app in action here. You can upload the image to the GitHub issue tracker and link it, or add it directly to the repo.]



---



\### ✨ Key Features



\*   \*\*🤖 Auto Weak-Labeling:\*\* Leverages the powerful \*\*Google Gemini 1.5 Flash\*\* model to generate initial labels for an entire unlabeled dataset.

\*   \*\*🧠 Active Learning Strategy:\*\* Implements an \*\*Uncertainty Sampling\*\* strategy to prioritize the review queue. The tool always presents the image with the lowest model confidence score first, maximizing the impact of human-in-the-loop feedback.

\*   \*\*⚡ Efficient User Interface:\*\* A clean and fast UI built with \*\*Streamlit\*\*, allowing users to quickly verify or correct AI-generated labels.

\*   \*\*📊 Progress Management:\*\* Automatically saves verified labels and tracks overall progress, allowing the annotation process to be paused and resumed.



---



\### 🛠️ Tech Stack



\*   \*\*Languages \& Frameworks:\*\* Python, Streamlit, Pandas, Jupyter

\*   \*\*Cloud Services \& APIs:\*\* Google Gemini 1.5 Flash API

\*   \*\*Core Libraries:\*\* `google-generativeai`, `pandas`, `streamlit`, `kaggle`



---



\### 🚀 Setup and Installation



\#### 1. Clone the Repository

```bash

git clone \[YOUR\_GITHUB\_REPOSITORY\_URL]

cd AI\_Dataset\_Annotator```



\#### 2. Create and Activate a Virtual Environment

```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# macOS/Linux

python3 -m venv venv

source venv/bin/activate

