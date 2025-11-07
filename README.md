
## 🎵 Music Royalty Automation System

**Music Royalty Automation** is an AI-powered tool that helps music managers, artists, and labels automatically parse royalty contracts and calculate fair payout distributions from streaming royalty statements.

Built with **GPT-4**, **Streamlit**, and **Python**, it simplifies one of the most painful parts of artist management — reading contracts and calculating splits.

---

### 🚀 Features

* **Upload multiple contracts at once** (PDF or Excel format)
* **Parse contracts automatically** to extract:

  * Parties involved (artists, producers, songwriters, etc.)
  * Works (songs, albums, EPs)
  * Streaming royalty splits (%)
* **Upload a distributor’s royalty statement (Excel)**
* **Automatically calculate payouts** for each contributor
* **Visualize results**:

  * Interactive **pie chart** of payout distribution
  * **Payment breakdown table** (exportable to Excel)
* **Detect missing or incomplete data** (e.g., missing contributor names or share percentages)

---

### 🧠 How It Works

1. The **Contract Parser** reads uploaded contract(s) using GPT-4 and extracts structured data (contributors, works, splits).
2. The **Royalty Calculator** reads the distributor’s royalty Excel sheet, matches songs, and computes the payout for each contributor based on their share.
3. The **Streamlit App** ties it all together with an easy-to-use interface for uploading, processing, and visualizing results.

---

### 🛠️ Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io)
* **AI Contract Parsing:** GPT-4 (via OpenAI API)
* **Data Processing:** Pandas, OpenPyXL
* **PDF Handling:** PyMuPDF (fitz)
* **Visualization:** Plotly

---

### ⚙️ Project Structure

```
royalty-automated-calculator/
│
├── src/
│   ├── app.py                      # Streamlit frontend
│   └── parser/
│       ├── contract_parser.py      # GPT-4 contract parser
│       ├── royalty_calculator.py   # Royalty payment calculator
│       └── __init__.py
│
├── .streamlit/
│   └── secrets.toml                # Local OpenAI API key (ignored in Git)
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

### 🧩 Installation

#### Clone the repository

```bash
git clone https://github.com/Niyokindi/royalty-automated-calculator.git
cd royalty-automated-calculator
```


#### Install dependencies

```bash
pip install -r requirements.txt
```

---

### 🔑 API Key Setup

The app uses the **OpenAI API** for contract parsing.

#### Option A: Local (recommended for development)

Create a `.streamlit/secrets.toml` file in your project root:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

#### Option B: Streamlit Cloud Deployment

Add your key directly in your Streamlit Cloud app’s **Secrets Manager** under:

```
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

⚠️ **Never commit your API key to GitHub.**
`.streamlit/secrets.toml` is automatically ignored in `.gitignore`.

---

### 🖥️ Running the App Locally

Once everything is set up, you can run the app using either command:

#### 🧩 Streamlit interface (recommended)

```bash
streamlit run src/app.py
```

#### 🐍 Command-line mode (for debugging)

```bash
python3 src/app.py
```

---

### 📊 Example Workflow

1. Upload your **contracts** (you can upload multiple PDFs if contributors have separate agreements).
2. Upload your **royalty statement** (Excel file from your distributor).
3. Click **“Calculate Payments”**.
4. The app will:

   * Parse all contracts
   * Merge contributor data
   * Match songs to the royalty statement
   * Display total payouts for each contributor
   * Let you **download an Excel report**

---

### 🧾 Output Example

| Contributor  | Role       | Work | Share % | Amount to Pay |
| ------------ | ---------- | ---- | ------- | ------------- |
| Romes Isaiah | Artist     | Home | 25%     | $3.48         |
| Lebron James | Producer   | Home | 25%     | $3.48         |
| Kenji        | Songwriter | Home | 20%     | $2.79         |

---

### 🧰 Troubleshooting

| Issue                       | Fix                                                      |
| --------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: fitz` | Run `pip install PyMuPDF`                                |
| `No secrets found`          | Create `.streamlit/secrets.toml` locally                 |
| `Push blocked (GitHub)`     | Remove `.streamlit/secrets.toml` from repo and re-commit |
| Incorrect payouts           | Ensure all contracts list **streaming splits** clearly   |

---

### 🧑‍💻 Author

**Kenji Niyokindi**
Founder, [Greenbox Analytics](https://www.linkedin.com/in/kenji-niyokindi/)
Toronto, Canada




