# AirInsights 🛩️

A comprehensive real-time airline market demand analysis platform powered by AI, featuring live flight tracking, advanced analytics, and intelligent market insights.

## 🚀 Overview

AirInsights is a full-stack web application that provides real-time airline market analysis using legitimate aviation APIs and Google Gemini AI. The platform offers live aircraft tracking, scheduled flight data, comprehensive analytics, and AI-powered market insights.

## ✨ Key Features

### 🛫 Real-time Flight Tracking
- **Live Aircraft Data**: Real-time positions from FlightRadar24 and OpenSky Network
- **Scheduled Flights**: Comprehensive flight schedules from AviationStack API
- **Geographic Filtering**: Focus on Australia and surrounding regions
- **Status Monitoring**: Track flight status, altitude, speed, and ground status

### 📊 Advanced Analytics
- **Market Trends**: Route popularity and demand analysis
- **Time-based Patterns**: Peak hours and seasonal trends
- **Airport Analytics**: High-demand locations and traffic patterns
- **Airline Performance**: Market share and competitive analysis

### 🤖 AI-Powered Insights
- **Intelligent Analysis**: Google Gemini AI for market insights
- **Pattern Recognition**: Hidden trends and opportunities
- **Predictive Analytics**: Market demand forecasting
- **Auto-scrolling Interface**: Smooth user experience

### 🎨 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Beautiful data visualizations with Recharts
- **Real-time Updates**: Live data refresh and status indicators
- **Error Handling**: User-friendly error messages and retry options

## 🏗️ Architecture

```
AirInsights/
├── airinsights-backend/     # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── flight_scraper.py   # Real-time flight data
│   ├── aviation.py         # AviationStack integration
│   ├── gemini.py           # Google Gemini AI
│   ├── utils.py            # Shared utilities
│   └── routes/             # API blueprints
├── airinsights-frontend/    # Next.js frontend
│   ├── app/                # Next.js app directory
│   ├── components/         # UI components
│   └── lib/                # Utility functions
└── CLEANUP_SUMMARY.md      # Codebase documentation
```

## 🛠️ Tech Stack

### Backend
- **Framework**: Python Flask
- **APIs**: AviationStack
- **AI**: Google Gemini AI
- **Data Processing**: Python Collections, Custom utilities
- **Deployment**: Gunicorn, Docker-ready

### Frontend
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + shadcn/ui
- **Charts**: Recharts for data visualization
- **HTTP Client**: Axios
- **Language**: TypeScript/JavaScript

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ and pip
- API keys for external services

### 1. Backend Setup

```bash
# Navigate to backend
cd airinsights-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "AVIATIONSTACK_API_KEY=your_key_here" > .env
echo "GEMINI_API_KEY=your_key_here" >> .env

# Start backend server
python app.py
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd airinsights-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📊 API Endpoints

### Core Endpoints
- `GET /flights` - Scheduled flights from AviationStack
- `GET /scraped` - Live aircraft data from multiple sources
- `POST /insights` - AI-powered market insights

### Analytics Endpoints
- `GET /flights/dashboard` - Comprehensive analytics data
- `GET /flights/analytics` - Flight statistics and trends
- `GET /flights/trends` - Market trend analysis

### Filtering Endpoints
- `GET /flights/filter` - Advanced flight filtering

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
GEMINI_API_KEY=your_gemini_api_key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### API Keys Required

1. **AviationStack API Key**
   - Sign up at [aviationstack.com](https://aviationstack.com)
   - Free tier available (100 requests/month)

2. **Google Gemini AI API Key**
   - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Free tier available

## 📈 Features in Detail

### Dashboard (`/dashboard`)
- **Real-time Data Fetching**: Get live aircraft and scheduled flights
- **Interactive Statistics**: Flight counts, airborne vs grounded aircraft
- **AI Insights Generation**: One-click AI analysis with auto-scrolling
- **Error Handling**: Graceful degradation when APIs are unavailable

### Analytics (`/analytics`)
- **Route Analysis**: Popular routes and demand patterns
- **Airport Analytics**: High-traffic airports and activity levels
- **Time Trends**: Peak departure hours and seasonal patterns
- **Market Insights**: Competitive analysis and price trends

### Data Sources
- **FlightRadar24**: Live aircraft positions and flight data
- **OpenSky Network**: Real-time ADS-B flight data
- **AviationStack**: Comprehensive flight schedules
- **Google Gemini AI**: Intelligent market analysis

## 🔍 Development

### Code Quality
- **Clean Architecture**: Modular design with clear separation
- **Error Handling**: Comprehensive error handling and logging
- **Type Safety**: TypeScript on frontend, type hints on backend
- **Documentation**: Well-documented code and APIs

### Testing
```bash
# Backend testing
curl http://localhost:5000/flights
curl http://localhost:5000/scraped
curl http://localhost:5000/flights/dashboard

# Frontend testing
npm run build
npm run lint
```

### Performance
- **Response Times**: 200ms-5s depending on endpoint
- **Caching**: Efficient data processing and caching
- **Rate Limiting**: Respectful API usage
- **Memory Management**: Optimized data structures

## 🔒 Security

- **Input Validation**: Comprehensive validation of all inputs
- **API Key Protection**: Secure handling of sensitive keys
- **CORS Configuration**: Proper cross-origin resource sharing
- **Error Handling**: Secure error messages without data exposure

## 🙏 Acknowledgments

- **AviationStack** for flight schedule data
- **Google Gemini AI** for intelligent analysis
- **Next.js** and **Flask** communities for excellent frameworks