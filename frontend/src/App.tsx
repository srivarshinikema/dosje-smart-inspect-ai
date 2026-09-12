import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div className="min-h-screen bg-gray-50 p-8"><h1 className="text-3xl font-bold">DoSJE SmartInspect AI - Frontend</h1><p className="mt-4">Dashboard coming soon...</p></div>} />
      </Routes>
    </Router>
  )
}

export default App
