import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getScripts, getCategories, verifyPassword } from '../api'

export const useStore = defineStore('main', () => {
  // 状态
  const scripts = ref([])
  const categories = ref([])
  const loading = ref(false)
  const searchQuery = ref('')
  const selectedCategory = ref(null)
  const isAdmin = ref(false)

  // 计算属性：根据搜索和分类过滤脚本
  const filteredScripts = computed(() => {
    let result = scripts.value
    if (selectedCategory.value) {
      result = result.filter(s => s.category_id === selectedCategory.value)
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(s =>
        s.title.toLowerCase().includes(q) ||
        s.description?.toLowerCase().includes(q) ||
        s.tags?.toLowerCase().includes(q)
      )
    }
    return result
  })

  // 获取脚本列表
  async function fetchScripts() {
    loading.value = true
    try {
      const { data } = await getScripts()
      scripts.value = data
    } catch (e) {
      console.error('获取脚本失败:', e)
    } finally {
      loading.value = false
    }
  }

  // 获取分类列表
  async function fetchCategories() {
    try {
      const { data } = await getCategories()
      categories.value = data
    } catch (e) {
      console.error('获取分类失败:', e)
    }
  }

  // 验证管理密码
  async function checkPassword(password) {
    try {
      await verifyPassword(password)
      sessionStorage.setItem('admin_password', password)
      isAdmin.value = true
      return true
    } catch {
      return false
    }
  }

  // 检查 session 中是否已有密码
  function restoreSession() {
    const password = sessionStorage.getItem('admin_password')
    if (password) {
      isAdmin.value = true
    }
  }

  // 获取分类名称
  function getCategoryName(id) {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : '未分类'
  }

  function getCategoryIcon(id) {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.icon : '📁'
  }

  return {
    scripts, categories, loading, searchQuery, selectedCategory, isAdmin,
    filteredScripts,
    fetchScripts, fetchCategories, checkPassword, restoreSession,
    getCategoryName, getCategoryIcon
  }
})
