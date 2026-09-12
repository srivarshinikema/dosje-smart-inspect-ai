export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: 'ADMIN' | 'GOVERNMENT_OFFICER' | 'INSPECTOR' | 'PROJECT_REPRESENTATIVE'
  is_active: number
  created_at: string
}

export interface Project {
  id: number
  name: string
  institute: string
  scheme: string
  location: string
  latitude: number
  longitude: number
  contact: string
  status: string
  risk_score: number
  compliance_status: string
}

export interface Inspection {
  id: number
  project_id: number
  inspector_id: number
  status: string
  inspection_date: string
  gps_latitude: number
  gps_longitude: number
  notes: string
}
