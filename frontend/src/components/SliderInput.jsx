import React from 'react'
import { Slider } from './ui/slider'
import { Label } from './ui/label'

export const SliderInput = ({ label, value, onChange, min, max, step = 1, description, darkMode = false }) => {
  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <Label className={darkMode ? 'text-gray-300' : 'text-gray-700'}>{label}</Label>
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          min={min}
          max={max}
          step={step}
          className={`w-20 px-2 py-1 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-medical-teal-500 ${
            darkMode
              ? 'bg-gray-700 border-gray-600 text-white'
              : 'bg-white border-gray-300'
          }`}
        />
      </div>
      <Slider
        value={[value]}
        onValueChange={([val]) => onChange(val)}
        min={min}
        max={max}
        step={step}
        className="w-full"
      />
      {description && (
        <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{description}</p>
      )}
    </div>
  )
}
