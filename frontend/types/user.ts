export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'admin' | 'manager' | 'receptionist' | 'professional' | 'customer';
  phone?: string;
  mobile?: string;
  is_active: boolean;
  date_joined: string;
  last_login?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  role?: string;
  phone?: string;
  mobile?: string;
}
