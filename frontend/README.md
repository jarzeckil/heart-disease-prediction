# Heart Failure Prediction - Frontend

Modern React frontend for the Heart Failure Prediction ML system.

## Tech Stack

- **React 18** with Vite
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Radix UI** for accessible components
- **Lucide React** for icons
- **Axios** for API calls

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Features

- 🏥 **Medical SaaS Design** - Clean, professional interface with teal accents
- 📊 **Interactive Form** - Dual-control sliders and numeric inputs for all parameters
- 📈 **Real-time Predictions** - Instant heart disease risk assessment
- 🔍 **SHAP Explanations** - Visual feature importance using SHAP values
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Built with Radix UI primitives and Tailwind CSS

## API Integration

The frontend connects to the FastAPI backend via proxy configuration in `vite.config.js`:
- `/predict` - Get heart disease prediction
- `/explain` - Get SHAP-based model explanation

Make sure the FastAPI backend is running on `http://localhost:8000` before using the app.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   │   ├── label.jsx
│   │   │   └── slider.jsx
│   │   └── SliderInput.jsx
│   ├── lib/
│   │   └── utils.js      # Utility functions
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles with Tailwind
├── public/
├── index.html
├── vite.config.js        # Vite configuration with proxy
├── tailwind.config.js    # Tailwind configuration
└── package.json
```

## Environment

The development server proxies API requests to avoid CORS issues. In production, configure your reverse proxy or API gateway accordingly.
