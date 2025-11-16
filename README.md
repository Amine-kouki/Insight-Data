# 🧠 Insight-Data: AI-Powered Data Analysis Agent [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://insight-data-hvcmh3jdckexqqkjmqnsbe.streamlit.app/)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Google Generative AI](https://img.shields.io/badge/Google_Generative_AI-Latest-yellow?style=flat-square&logo=google)](https://ai.google.dev/)

> **Intelligent CSV analysis powered by AI** — Ask natural language questions about your data and get instant visualizations, analysis, and professional PDF reports.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 What It Does](#-what-it-does)
- [⚙️ Installation](#️-installation)
- [🚀 Quick Start](#-quick-start)
- [📊 Usage Examples](#-usage-examples)
- [🧰 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [⭐ Acknowledgements](#-acknowledgements)

---

## ✨ Features

- 🤖 **AI-Powered Natural Language Processing** — Ask questions in plain English, the AI generates pandas code automatically
- 📊 **Dynamic Visualizations** — Create interactive Plotly charts with a single query
- 📈 **Instant Data Analysis** — Get professional insights and business implications for your data
- 🎨 **Beautiful Reports** — Generate polished PDF reports with tables, charts, and analysis
- 📋 **Markdown Support** — Reports with formatted headers, bullet points, and structured sections
- 🛒 **Report Cart System** — Build multi-page reports by adding multiple analyses
- 🔄 **Session Persistence** — Save your analysis items and generate reports at any time

---

## 🎯 What It Does

**Insight-Data** is an intelligent data analysis assistant that bridges the gap between raw data and actionable insights. Here's the workflow:

1. **Upload CSV** → Load your dataset
2. **Ask Questions** → Use natural language (e.g., *"Show me average sales by region"*)
3. **AI Generates Code** → The agent creates pandas/plotly code automatically
4. **View Results** → See tables, charts, and AI-generated analysis
5. **Build Reports** → Add multiple analyses to a cart
6. **Export PDF** → Download a professional report with all your findings

---

## ⚙️ Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Google Generative AI API Key** (get one [here](https://ai.google.dev/))
- **Kaleido** (for PDF export — installed via pip)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Amine-kouki/Insight-Data.git
cd Insight-Data
```

### Step 2: Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Google Generative AI API key.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will start at `http://localhost:8501` 🎉

---

## 🚀 Quick Start

### Basic Usage

1. **Open the app** → Visit `http://localhost:8501` in your browser
2. **Upload a CSV file** → Click the file uploader
3. **View data preview** → See the first 5 rows automatically
4. **Ask a question** → Type a query like:
   - *"What is the average sales per region?"*
   - *"Show me the top 10 products by revenue"*
   - *"Plot customer acquisition over time"*
5. **View results** → Charts, tables, and analysis appear instantly
6. **Add to report** → Click *"Add to Report"* to include in your PDF
7. **Generate PDF** → Use the sidebar to download your report

### Example Queries

```
"Plot the profit (sales - cost) for each product"
"What is the average sales for each region?"
"Show me the first 5 rows"
"Calculate total revenue by category"
"Create a line chart of monthly trends"
"Find the top 10 customers by spending"
```

---

## 📊 Usage Examples

### Example 1: Generating a Chart

```
User Query: "Plot the average sales for each region"
↓
AI generates pandas/plotly code automatically
↓
Interactive chart displayed in Streamlit
↓
Professional analysis added by AI
↓
One click to add to report
```

### Example 2: Building a Multi-Section Report

1. Upload `sales_data.csv`
2. Ask: *"What are our top 5 products?"* → Add to report ✓
3. Ask: *"Show sales trends over time"* → Add to report ✓
4. Ask: *"Calculate profit by region"* → Add to report ✓
5. Click **"Generate PDF Report"** in the sidebar
6. Download `data_analysis_report.pdf` with all three analyses

---

https://github.com/user-attachments/assets/4f133033-ca03-4880-8341-880bcbbf3f8b

---
## 🧰 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) | Data manipulation & analysis |
| **Visualization** | [Plotly](https://plotly.com/) | Interactive charts & graphs |
| **AI/ML** | [Google Generative AI](https://ai.google.dev/) | Natural language code generation & analysis |
| **PDF Generation** | [ReportLab](https://www.reportlab.com/) | Professional PDF reports |
| **Environment** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Secure API key management |
| **Chart Export** | [Kaleido](https://github.com/plotly/Kaleido) | Static image export for PDFs |

---

## 📁 Project Structure

```
Insight-Data/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── agent_logic/
│   ├── __init__.py
│   ├── prompts.py                 # AI system prompts & instructions
│   └── analysis_agent.py           # AI agent functions for code generation
├── report_builder/
│   ├── __init__.py
│   ├── pdf_utils.py               # PDF utility functions
│   └── pdf_generator.py            # PDF report generation logic
└── venv/                          # Virtual environment (auto-created)
```

### Key Files

- **`app.py`** — Main application entry point with Streamlit UI
- **`agent_logic/prompts.py`** — System prompts that guide the AI model
- **`agent_logic/analysis_agent.py`** — Functions to generate code and analysis using Google Generative AI
- **`report_builder/pdf_generator.py`** — PDF report generation with formatting

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**: `git commit -m "Add feature: description"`
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Open a Pull Request** with a detailed description of changes

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes before submitting
- Update documentation if needed
- Be respectful and constructive

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use this project commercially
- ✅ Modify the source code
- ✅ Distribute the code
- ⚠️ Just include a copy of the license and acknowledge the original authors

---

## ⭐ Acknowledgements

- **Google Generative AI** — For the powerful `gemini-flash-latest` model
- **Streamlit** — For the amazing web framework
- **Plotly** — For interactive visualization library
- **ReportLab** — For PDF generation capabilities
- **Pandas** — For data manipulation excellence

### Inspiration

This project was inspired by the need to make data analysis accessible to non-technical users through conversational AI.

---

## 📞 Support & Questions

- 💬 **Issues** — Report bugs or request features on [GitHub Issues](https://github.com/Amine-kouki/Insight-Data/issues)
- 📧 **Email** — [Contact Us](mailto:amine.kouki.org@outlook.com)
- 📚 **Documentation** — Check inline code comments and docstrings

---

## 🎯 Roadmap

### Upcoming Features (Planned)

- [ ] **Database Support** — Connect to PostgreSQL, MySQL, MongoDB
- [ ] **Advanced Filtering** — UI-based data filtering before analysis
- [ ] **Custom Themes** — User-selectable report themes
- [ ] **Scheduled Reports** — Automated report generation on schedule
- [ ] **Team Collaboration** — Share reports and analyses with team members
- [ ] **Version History** — Track analysis changes over time
- [ ] **Export Formats** — Excel, PowerPoint, and HTML export options
- [ ] **Data Quality Checks** — Automated data validation and profiling

---

<div align="center">

**Built by [Amine Kouki](https://github.com/Amine-kouki)**

[⭐ Star us on GitHub](https://github.com/Amine-kouki/Insight-Data) • [🐛 Report a Bug](https://github.com/Amine-kouki/Insight-Data/issues) • [💡 Request a Feature](https://github.com/Amine-kouki/Insight-Data/issues)

</div>
