# NetworkGraphs

**NetworkGraphs** is a web-based application that allows users to upload documents (e.g., text files, PDFs) and visualize the relationships between key entities in the form of a network graph. It’s useful for exploring connections between people, places, topics, or other extracted terms.

🌐 **Live Demo**: [https://network-graphs.onrender.com/](https://network-graphs.onrender.com/)

---

## 🚀 Features

- Upload and process documents (`.txt`, `.pdf`)
- Extract named entities or keywords using NLP
- Generate interactive network graphs
- Visualize relationships between entities
- Simple and intuitive web interface

---

## 🛠️ Technologies Used

- **Frontend**  
  - HTML, CSS, JavaScript  
  - [Cytoscape.js](https://js.cytoscape.org/) for interactive graph rendering  

- **Backend**  
  - Python 3  
  - [FastAPI](https://fastapi.tiangolo.com/) & Uvicorn for the web server  
  - [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction  
  - [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation  
  - python-dotenv for environment variable management  

- **Graph Extraction**  
  - OpenAI ChatCompletion API (e.g. `gpt-3.5-turbo`) for entity & relationship extraction  

- **Deployment**  
  - Render.com (Docker-compatible hosting)

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aman-Khokhar18/networkgraphs.git
   cd networkgraphs
