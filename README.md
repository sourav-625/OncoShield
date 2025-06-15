# 🛡️ OncoShield – Non-Invasive Tumor Detection System

OncoShield is a non-invasive, AI-based cancer screening system that integrates **Thermography**, **Near-Infrared Spectroscopy (NIR)**, and **Electrical Impedance Spectroscopy (EIS)** to provide early-stage cancer risk detection. It uses a hybrid machine learning model and is built with a modern web interface to make early diagnosis more accessible, affordable, and scalable.

---

## 🚀 Features

- 🌡️ Combines multiple non-invasive sensing technologies (Thermal, NIR, EIS)
- 🤖 AI-based prediction using CNN and LSTM
- 💻 Frontend built with **React.js** for real-time interaction (under development)
- 📊 Time-windowed analysis for greater diagnostic accuracy
- ☁️ Backend and cloud-hosted ML model (planned)

---

## 🧠 Technologies Used

### 🔷 Frontend *(in development)*
- React.js
- JavaScript (ES6+)
- TailwindCSS / Material UI (optional)
- Axios (for API calls)
- Git & GitHub

### 🔶 Backend *(in development)*
- Node.js + Express.js for API development
- MongoDB or Firebase for database
- Cloud-hosted ML inference (Flask/TensorFlow Serving API)
- Authentication and user management

### ⚙️ Machine Learning Model *(Recently Integrated)*
- CNN for image-based thermography & NIR input
- LSTM for sequential EIS signal data
- Ensemble Learning for final classification

---

## 🧬 ML Model Pipeline *(currently icludes core components - expansions planned)*
[ NIR/Infrared Image ]      [ EIS Time-Series ]
↓ ↓                               ↓ ↓
CNN Model                     LSTM Model
↓ ↓                               ↓ ↓
→→→→→→→→→→→ Ensemble Learning →→→→→→→→→→→→
               ↓
Final Cancer Risk Prediction

## 💻 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/OncoShield.git
cd OncoShield
```

### 2. Install Dependencies
```bash
cd frontend
npm install
```

### 3. Run the App
```bash
npm start
```

## Project Structure
OncoShield/
├── frontend/           # React app
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
├── backend/            # (Planned: Node/Express API)
├── ml-model/           # (Planned: ML model & training code)
├── assets/             # Images, icons, logos
└── README.md

## 🤝 Contributing
Contributions are welcome!
- 1.Fork the repo
- 2.Create a new branch
- 3.Commit your changes
- 4.Submit a pull request

## 📬 Contact
Developer: Sourav Pati
📧 Email: [k0259.mpsbls@gamil.com](k0259.mpsbls@gmail.com)
🌐 GitHub: [sourav-625](https://github.com/sourav-625)
