<template>
  <div class="min-h-screen pb-20">
    <!-- 头部 -->
    <header class="pt-12 pb-8 px-6 text-center">
      <h1 class="text-4xl font-bold bg-gradient-to-r from-flower-500 via-purple-500 to-blue-500 bg-clip-text text-transparent mb-2">
        Flowers
      </h1>
      <p class="text-gray-500 text-sm">每个脚本都是一朵花，每朵花都不一样</p>

      <!-- 搜索框 -->
      <div class="mt-6 max-w-md mx-auto relative">
        <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          v-model="store.searchQuery"
          placeholder="搜索脚本..."
          class="w-full pl-12 pr-4 py-3 rounded-2xl bg-white/70 backdrop-blur border border-white/50 shadow-sm focus:border-flower-300 focus:ring-2 focus:ring-flower-200 outline-none transition text-sm"
        />
      </div>
    </header>

    <!-- 分类筛选 -->
    <div class="px-6 mb-8">
      <div class="max-w-4xl mx-auto flex flex-wrap items-center gap-2 justify-center">
        <button
          @click="store.selectedCategory = null"
          :class="[
            'px-4 py-1.5 rounded-full text-sm transition font-medium',
            !store.selectedCategory
              ? 'bg-white text-gray-800 shadow-sm'
              : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
          ]"
        >
          全部
        </button>
        <button
          v-for="cat in store.categories"
          :key="cat.id"
          @click="store.selectedCategory = store.selectedCategory === cat.id ? null : cat.id"
          :class="[
            'px-4 py-1.5 rounded-full text-sm transition font-medium',
            store.selectedCategory === cat.id
              ? 'bg-white text-gray-800 shadow-sm'
              : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
          ]"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>

        <!-- 管理分类按钮 -->
        <button
          v-if="store.isAdmin"
          @click="showCategoryManager = true"
          class="px-3 py-1.5 rounded-full text-sm text-gray-400 hover:text-gray-600 hover:bg-white/50 transition"
          title="管理分类"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 脚本网格 -->
    <main class="px-6">
      <div class="max-w-5xl mx-auto">
        <!-- 加载中 -->
        <div v-if="store.loading" class="text-center py-20">
          <div class="inline-block w-8 h-8 border-3 border-flower-300 border-t-transparent rounded-full animate-spin"></div>
          <p class="text-gray-400 text-sm mt-3">加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="store.filteredScripts.length === 0" class="text-center py-20">
          <div class="text-5xl mb-4">🌱</div>
          <p class="text-gray-500">{{ store.searchQuery ? '没有找到匹配的脚本' : '花园还是空的，种下第一朵花吧' }}</p>
        </div>

        <!-- 脚本卡片网格 -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <ScriptCard
            v-for="script in store.filteredScripts"
            :key="script.id"
            :script="script"
            @click="openDetail"
            class="fade-in"
          />
        </div>
      </div>
    </main>

    <!-- 新增按钮 (FAB) -->
    <button
      @click="handleAdd"
      class="fixed right-6 bottom-6 w-14 h-14 bg-gradient-to-r from-flower-400 to-flower-500 text-white rounded-full shadow-lg hover:shadow-xl hover:from-flower-500 hover:to-flower-600 transition-all flex items-center justify-center text-2xl"
      title="新增脚本"
    >
      +
    </button>

    <!-- 弹窗 -->
    <PasswordDialog
      :show="showPasswordDialog"
      @close="showPasswordDialog = false"
      @success="onPasswordSuccess"
    />

    <ScriptDetail
      :show="showDetail"
      :script="selectedScript"
      @close="showDetail = false"
      @edit="handleEdit"
      @delete="handleDelete"
    />

    <ScriptForm
      :show="showForm"
      :script="editingScript"
      @close="showForm = false"
      @saved="onScriptSaved"
    />

    <CategoryManager
      :show="showCategoryManager"
      @close="showCategoryManager = false"
      @updated="store.fetchCategories()"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from './stores'
import { deleteScript } from './api'
import ScriptCard from './components/ScriptCard.vue'
import ScriptDetail from './components/ScriptDetail.vue'
import ScriptForm from './components/ScriptForm.vue'
import PasswordDialog from './components/PasswordDialog.vue'
import CategoryManager from './components/CategoryManager.vue'

const store = useStore()

const showPasswordDialog = ref(false)
const showDetail = ref(false)
const showForm = ref(false)
const showCategoryManager = ref(false)
const selectedScript = ref(null)
const editingScript = ref(null)
const pendingAction = ref(null)

onMounted(() => {
  store.restoreSession()
  store.fetchScripts()
  store.fetchCategories()
})

function openDetail(script) {
  selectedScript.value = script
  showDetail.value = true
}

function requireAdmin(action) {
  if (store.isAdmin) {
    action()
  } else {
    pendingAction.value = action
    showPasswordDialog.value = true
  }
}

function onPasswordSuccess() {
  if (pendingAction.value) {
    pendingAction.value()
    pendingAction.value = null
  }
}

function handleAdd() {
  requireAdmin(() => {
    editingScript.value = null
    showForm.value = true
  })
}

function handleEdit(script) {
  showDetail.value = false
  requireAdmin(() => {
    editingScript.value = script
    showForm.value = true
  })
}

async function handleDelete(script) {
  showDetail.value = false
  requireAdmin(async () => {
    if (!confirm(`确认删除「${script.title}」？`)) return
    try {
      await deleteScript(script.id)
      await store.fetchScripts()
    } catch (e) {
      alert('删除失败: ' + (e.response?.data?.detail || e.message))
    }
  })
}

async function onScriptSaved() {
  await store.fetchScripts()
}
</script>
