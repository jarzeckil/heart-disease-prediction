import React, { useState } from 'react'
import axios from 'axios'
import { Heart, Activity, AlertCircle, TrendingUp, Info } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { SliderInput } from './components/SliderInput'
import { Label } from './components/ui/label'

function App() {
  // Form state
  const [formData, setFormData] = useState({
    Age: 45,
    Sex: 'M',
    ChestPainType: 'ATA',
    RestingBP: 130,
    Cholesterol: 230,
    FastingBS: 0,
    RestingECG: 'Normal',
    MaxHR: 140,
    ExerciseAngina: 'N',
    Oldpeak: 1.5,
    ST_Slope: 'Flat'
  })

  // Results state
  const [prediction, setPrediction] = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)
    setExplanation(null)

    try {
      // First, get prediction
      const predictionResponse = await axios.post('/predict', formData)
      setPrediction(predictionResponse.data)

      // Then, get explanation
      const explanationResponse = await axios.post('/explain', formData)
      setExplanation(explanationResponse.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const updateFormData = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  // Prepare data for prediction chart
  const predictionChartData = prediction ? [
    {
      name: 'Healthy',
      probability: ((prediction['Probability-negative'] || 0) * 100).toFixed(1),
      fill: '#10b981'
    },
    {
      name: 'Heart Disease',
      probability: ((prediction['Probability-positive'] || 0) * 100).toFixed(1),
      fill: '#ef4444'
    }
  ] : []

  // Prepare data for SHAP chart
  const shapChartData = explanation ?
    Object.entries(explanation)
      .map(([feature, value]) => ({
        feature,
        value: parseFloat(typeof value === 'number' ? value : parseFloat(value)),
        fill: value > 0 ? '#ef4444' : '#10b981'
      }))
      .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    : []

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-medical-teal-100 rounded-lg">
              <Heart className="w-8 h-8 text-medical-teal-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Heart Failure Prediction</h1>
              <p className="text-sm text-gray-600 mt-1">AI-powered cardiovascular risk assessment</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Form */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
              <div className="flex items-center space-x-2 mb-6">
                <Activity className="w-5 h-5 text-medical-teal-600" />
                <h2 className="text-xl font-semibold text-gray-900">Patient Information</h2>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Age */}
                <SliderInput
                  label="Age"
                  value={formData.Age}
                  onChange={(val) => updateFormData('Age', val)}
                  min={1}
                  max={120}
                  step={1}
                  description="Age of the patient in years"
                />

                {/* Sex */}
                <div className="space-y-2">
                  <Label className="text-gray-700">Sex</Label>
                  <select
                    value={formData.Sex}
                    onChange={(e) => updateFormData('Sex', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>

                {/* Chest Pain Type */}
                <div className="space-y-2">
                  <Label className="text-gray-700">Chest Pain Type</Label>
                  <select
                    value={formData.ChestPainType}
                    onChange={(e) => updateFormData('ChestPainType', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value="TA">Typical Angina (TA)</option>
                    <option value="ATA">Atypical Angina (ATA)</option>
                    <option value="NAP">Non-Anginal Pain (NAP)</option>
                    <option value="ASY">Asymptomatic (ASY)</option>
                  </select>
                </div>

                {/* Resting BP */}
                <SliderInput
                  label="Resting Blood Pressure"
                  value={formData.RestingBP}
                  onChange={(val) => updateFormData('RestingBP', val)}
                  min={80}
                  max={200}
                  step={1}
                  description="Resting blood pressure in mm Hg"
                />

                {/* Cholesterol */}
                <SliderInput
                  label="Cholesterol"
                  value={formData.Cholesterol || 0}
                  onChange={(val) => updateFormData('Cholesterol', val)}
                  min={0}
                  max={600}
                  step={1}
                  description="Serum cholesterol in mm/dl (0 if unknown)"
                />

                {/* Fasting BS */}
                <div className="space-y-2">
                  <Label className="text-gray-700">Fasting Blood Sugar</Label>
                  <select
                    value={formData.FastingBS}
                    onChange={(e) => updateFormData('FastingBS', Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value={0}>≤ 120 mg/dl</option>
                    <option value={1}>&gt; 120 mg/dl</option>
                  </select>
                </div>

                {/* Resting ECG */}
                <div className="space-y-2">
                  <Label className="text-gray-700">Resting ECG</Label>
                  <select
                    value={formData.RestingECG}
                    onChange={(e) => updateFormData('RestingECG', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value="Normal">Normal</option>
                    <option value="ST">ST-T Wave Abnormality (ST)</option>
                    <option value="LVH">Left Ventricular Hypertrophy (LVH)</option>
                  </select>
                </div>

                {/* Max HR */}
                <SliderInput
                  label="Maximum Heart Rate"
                  value={formData.MaxHR}
                  onChange={(val) => updateFormData('MaxHR', val)}
                  min={60}
                  max={202}
                  step={1}
                  description="Maximum heart rate achieved (60-202)"
                />

                {/* Exercise Angina */}
                <div className="space-y-2">
                  <Label className="text-gray-700">Exercise-Induced Angina</Label>
                  <select
                    value={formData.ExerciseAngina}
                    onChange={(e) => updateFormData('ExerciseAngina', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value="N">No</option>
                    <option value="Y">Yes</option>
                  </select>
                </div>

                {/* Oldpeak */}
                <SliderInput
                  label="Oldpeak (ST Depression)"
                  value={formData.Oldpeak}
                  onChange={(val) => updateFormData('Oldpeak', val)}
                  min={-3}
                  max={7}
                  step={0.1}
                  description="ST depression induced by exercise"
                />

                {/* ST Slope */}
                <div className="space-y-2">
                  <Label className="text-gray-700">ST Slope</Label>
                  <select
                    value={formData.ST_Slope}
                    onChange={(e) => updateFormData('ST_Slope', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500"
                  >
                    <option value="Up">Upsloping</option>
                    <option value="Flat">Flat</option>
                    <option value="Down">Downsloping</option>
                  </select>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-medical-teal-600 hover:bg-medical-teal-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <TrendingUp className="w-5 h-5" />
                      <span>Predict Risk</span>
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-5 h-5 text-red-600" />
                  <h3 className="text-lg font-semibold text-red-900">Error</h3>
                </div>
                <p className="mt-2 text-sm text-red-700">{error}</p>
              </div>
            )}

            {!prediction && !loading && !error && (
              <div className="bg-white rounded-xl shadow-md p-8 border border-gray-200 text-center">
                <div className="flex justify-center mb-4">
                  <div className="p-4 bg-gray-100 rounded-full">
                    <Info className="w-12 h-12 text-gray-400" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">No Prediction Yet</h3>
                <p className="text-gray-500">Fill in the patient information and click "Predict Risk" to see results</p>
              </div>
            )}

            {prediction && (
              <>
                {/* Prediction Result Card */}
                <div className={`rounded-xl shadow-md p-6 border-2 ${
                  prediction.HeartDisease === 1
                    ? 'bg-red-50 border-red-300'
                    : 'bg-green-50 border-green-300'
                }`}>
                  <div className="flex items-center space-x-3 mb-4">
                    <Heart className={`w-6 h-6 ${
                      prediction.HeartDisease === 1 ? 'text-red-600' : 'text-green-600'
                    }`} />
                    <h3 className="text-xl font-semibold text-gray-900">Prediction Result</h3>
                  </div>
                  <div className="text-center py-4">
                    <p className={`text-4xl font-bold mb-2 ${
                      prediction.HeartDisease === 1 ? 'text-red-700' : 'text-green-700'
                    }`}>
                      {prediction.HeartDisease === 1 ? 'Heart Disease Risk' : 'Healthy'}
                    </p>
                    <p className="text-gray-600">
                      {prediction.HeartDisease === 1
                        ? `${((prediction['Probability-positive'] || 0) * 100).toFixed(1)}% probability of heart disease`
                        : `${((prediction['Probability-negative'] || 0) * 100).toFixed(1)}% probability of being healthy`
                      }
                    </p>
                  </div>
                </div>

                {/* Prediction Probabilities Chart */}
                <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Probabilities</h3>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={predictionChartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis label={{ value: 'Probability (%)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Bar dataKey="probability" radius={[8, 8, 0, 0]}>
                        {predictionChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* SHAP Explanation */}
                {explanation && (
                  <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <div className="flex items-center space-x-2 mb-4">
                      <Activity className="w-5 h-5 text-medical-teal-600" />
                      <h3 className="text-lg font-semibold text-gray-900">Feature Importance (SHAP)</h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Red bars increase risk, green bars decrease risk
                    </p>
                    <ResponsiveContainer width="100%" height={400}>
                      <BarChart
                        data={shapChartData}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" label={{ value: 'SHAP Value', position: 'insideBottom', offset: -5 }} />
                        <YAxis type="category" dataKey="feature" />
                        <Tooltip />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                          {shapChartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center space-y-3">
            <p className="text-sm text-gray-600">
              Heart Failure Prediction System • Powered by Machine Learning
            </p>
            <div className="flex items-center justify-center space-x-2 text-xs text-amber-700 bg-amber-50 py-2 px-4 rounded-lg max-w-2xl mx-auto">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <p>
                <strong>Medical Disclaimer:</strong> This tool is for educational and research purposes only.
                It is not a substitute for professional medical advice, diagnosis, or treatment.
              </p>
            </div>
            <a
              href="https://github.com/jarzeckil/heart-failure-prediction"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 text-sm text-medical-teal-600 hover:text-medical-teal-700 transition-colors"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              <span>View on GitHub</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
