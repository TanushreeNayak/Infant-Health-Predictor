import api from "./api"
import { useState } from "react";

export default function App() {

  const[predict, setPredict] = useState(null)  

  async function getPrediction(formData) {
    const obj = Object.fromEntries(formData)

    const payload = {
      age_months: parseFloat(obj.age),
      weight_kg: parseFloat(obj.weight),
      height_cm: parseFloat(obj.height),
      heart_rate: parseFloat(obj["heart-rate"]),
      oxygen_level: parseFloat(obj.oxy),
      temperature: parseFloat(obj.temp),
      feeding_frequency: parseFloat(obj.feeding),
      sleep_hours: parseFloat(obj.sleep)
    };

    try {
      const res = await api.post("/predicts", payload, {
        headers: { "Content-Type": "application/json" }
      });
      // Handle the prediction result here
      setPredict(res.data["Predicted Outcome"])
    } catch (err) {
      console.error("Error", err);
    }
    
  }
  return (
    <div className="px-80 py-10 ">
      <div className="bg-neutral-100 rounded-2xl border border-t-neutral-50 border-neutral-200 shadow-xl">
        <h1 className="text-center pt-4 text-3xl font-bold mb-2">👶 Infant Health Predictor 🩺</h1>
        <form className="grid grid-cols-1" onSubmit={e => {
          e.preventDefault()
          getPrediction(new FormData(e.target))
          e.target.reset()
        }}>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="age">Age(months):</label>
            <input className="border rounded-sm border-neutral-400 p-2" name="age" step="0.1" required min="6" max="12" type="number" id="age" placeholder="6-12"/>

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="weight">Weight(kg):</label>
            <input className="border rounded-sm border-neutral-400 p-2" name ="weight" step="0.1" required min="5.5" max="10" type="number" placeholder="5.5-10" id= "weight"/>

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="height">Height(cm):</label>
            <input className="border rounded-sm border-neutral-400 p-2" name="height" step="0.1" type="number" required min="60" max="80" placeholder="60-80" id="height" />

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="heart-rate">Heart Rate(bpm):</label>
            <input className="border rounded-sm border-neutral-400 p-2" name="heart-rate" step="0.1" required min="90" max="160" placeholder="90-160" type="number" id="heart-rate" />

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="oxy">Oxygen Level(%)</label>
            <input className="border rounded-sm border-neutral-400 p-2" step="0.1" name="oxy" required min="85" max="100" placeholder="85-100" type="number" id="oxy" />

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="temp">Temperature(c)</label>
            <input className="border rounded-sm border-neutral-400 p-2" step="0.1" name="temp" placeholder="36-39" required min="36" max="39" type="number" id="temp" />

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="feeding">Feeding Frequency(per day)</label>
            <input className="border rounded-sm border-neutral-400 p-2" step="0.1" name="feeding" required min="5" max="12" placeholder="5-12" type="number" id="feeding" />

          </div>
          <div className="grid grid-cols-1 p-4 rounded-lg mx-4 mt-1">
            <label className="text-lg font-medium text-neutral-700" htmlFor="sleep">Sleep Hours(per day):</label>
            <input className="border rounded-sm border-neutral-400 p-2" step="0.1" name="sleep" placeholder="10-15" required min= "10" max="15" type="number" id="sleep" />

          </div>
          <div className="w-auto text-center">
            <button className="border p-2 px-5 text-lg text-neutral-900 rounded-sm mb-6 mt-5 bg-indigo-200 border-neutral-100 hover:bg-indigo-300 font-medium">Get Prediction</button>

          </div>
        </form>
        {predict?<div className="text-center w-auto mx-40">
          <h3 className=" text-neutral-800 border-neutral-300 p-2 text-md rounded-sm mb-10 bg-indigo-300 font-medium">
            {`Prediction: ${predict}`}  
          </h3>
          </div>:null}
      </div>
    </div>
  )
}