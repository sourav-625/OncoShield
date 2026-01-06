# 🛡️ OncoShield – Non-Invasive Tumor Detection System

OncoShield is a non-invasive, AI-based Tumor Detection System that integrates **Thermography**, **Near-Infrared Spectroscopy (NIR)**, and **Electrical Impedance Spectroscopy (EIS)** to provide early-stage Tumor  detection. It uses a hybrid machine learning model and is built with a modern web interface to make early diagnosis more accessible, affordable, and scalable.

---

## 🚀 Features

- 🌡️ Combines multiple non-invasive sensing technologies (Thermal, NIR, EIS)
- 🤖 AI-based prediction using CNN and LSTM
- 💻 Frontend built with **React.js** for real-time interaction (under development)
- 📊 Time-windowed analysis for greater diagnostic accuracy
- ☁️ Backend and cloud-hosted ML model (planned)

---

## 🧬 ML Model Pipeline *(currently icludes core components)*
```text
[ NIR/Infrared Image ]      [ EIS Time-Series ]
↓ ↓                               ↓ ↓
CNN Model                     LSTM Model
↓ ↓                               ↓ ↓
→→→→→→→→→→→ Ensemble Learning →→→→→→→→→→→→
                   ↓
            Final Prediction
```

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


> **Disclaimer:**  
> This project is intended solely for **educational and research purposes**.  
> It has **not been reviewed, tested, or approved by any certified medical professionals or regulatory bodies**.  
> The system is **not intended for clinical diagnosis** and should **not be used to make medical decisions**.  
> Additionally, the current model may **not be capable of detecting all tumor types** or conditions, especially deep internal tumors or cancers.
