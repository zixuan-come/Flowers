import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 从 sessionStorage 读取密码，自动附加到请求头
api.interceptors.request.use(config => {
  const password = sessionStorage.getItem('admin_password')
  if (password) {
    config.headers['X-Admin-Password'] = password
  }
  return config
})

// --- 公开接口 ---

export function getScripts(params = {}) {
  return api.get('/scripts', { params })
}

export function getScript(id) {
  return api.get(`/scripts/${id}`)
}

export function getCategories() {
  return api.get('/categories')
}

// --- 受保护接口 ---

export function createScript(data) {
  return api.post('/scripts', data)
}

export function updateScript(id, data) {
  return api.put(`/scripts/${id}`, data)
}

export function deleteScript(id) {
  return api.delete(`/scripts/${id}`)
}

export function createCategory(data) {
  return api.post('/categories', data)
}

export function updateCategory(id, data) {
  return api.put(`/categories/${id}`, data)
}

export function deleteCategory(id) {
  return api.delete(`/categories/${id}`)
}

export function verifyPassword(password) {
  return api.post('/verify-password', { password })
}
