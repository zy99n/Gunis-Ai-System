import request from '@/utils/request'

export interface RegisterData {
  username: string
  email: string
  password: string
  nickname?: string
}

export interface LoginData {
  username_or_email: string
  password: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  nickname?: string
  avatar?: string
  is_active: boolean
  is_admin: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

// 用户注册
export const register = (data: RegisterData) => {
  return request.post<UserInfo>('/auth/register', data)
}

// 用户登录
export const login = (data: LoginData) => {
  return request.post<LoginResponse>('/auth/login', data)
}

// 获取当前用户信息
export const getMe = () => {
  return request.get<UserInfo>('/auth/me')
}

// 用户登出
export const logout = () => {
  return request.post('/auth/logout')
}