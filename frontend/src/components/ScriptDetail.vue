<template>
  <Transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center modal-mask" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl w-[90vw] max-w-[800px] max-h-[85vh] overflow-hidden fade-in flex flex-col">
        <!-- 头部 -->
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h2 class="text-xl font-bold text-gray-800">{{ script?.title }}</h2>
                <span
                  class="text-xs px-2.5 py-1 rounded-full font-mono font-medium"
                  :class="`lang-${script?.language?.toLowerCase() || 'default'}`"
                >
                  {{ script?.language || 'text' }}
                </span>
              </div>
              <p class="text-gray-500 text-sm">{{ script?.description || '暂无描述' }}</p>
              <div class="flex items-center gap-4 mt-3">
                <span class="text-sm text-gray-400">
                  {{ getCategoryIcon(script?.category_id) }} {{ getCategoryName(script?.category_id) }}
                </span>
                <span class="text-sm text-gray-400">{{ formatDate(script?.created_at) }}</span>
                <div v-if="script?.tags" class="flex gap-1.5">
                  <span
                    v-for="tag in tagList"
                    :key="tag"
                    class="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500"
                  >
                    #{{ tag }}
                  </span>
                </div>
              </div>
            </div>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition p-1">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- 代码区 -->
        <div class="flex-1 overflow-auto p-6">
          <div class="relative code-block bg-[#0d1117] rounded-xl">
            <button
              @click="copyCode"
              class="absolute top-3 right-3 px-3 py-1.5 bg-white/10 hover:bg-white/20 text-white/70 hover:text-white rounded-lg text-xs transition flex items-center gap-1.5"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
              {{ copied ? '已复制' : '复制' }}
            </button>
            <pre class="font-mono text-sm"><code v-html="highlightedCode"></code></pre>
          </div>
        </div>

        <!-- 底部操作 -->
        <div v-if="store.isAdmin" class="p-4 border-t border-gray-100 flex justify-end gap-3">
          <button
            @click="$emit('edit', script)"
            class="px-4 py-2 text-sm bg-blue-50 text-blue-600 rounded-xl hover:bg-blue-100 transition font-medium"
          >
            编辑
          </button>
          <button
            @click="$emit('delete', script)"
            class="px-4 py-2 text-sm bg-red-50 text-red-600 rounded-xl hover:bg-red-100 transition font-medium"
          >
            删除
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useStore } from '../stores'
import hljs from 'highlight.js'

const props = defineProps({ show: Boolean, script: Object })
defineEmits(['close', 'edit', 'delete'])
const store = useStore()
const copied = ref(false)

const { getCategoryName, getCategoryIcon } = store

const tagList = computed(() => {
  if (!props.script?.tags) return []
  return props.script.tags.split(',').map(t => t.trim()).filter(Boolean)
})

const highlightedCode = computed(() => {
  if (!props.script?.code) return ''
  const lang = props.script.language?.toLowerCase() || 'plaintext'
  try {
    if (hljs.getLanguage(lang)) {
      return hljs.highlight(props.script.code, { language: lang }).value
    }
    return hljs.highlightAuto(props.script.code).value
  } catch {
    return props.script.code
  }
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

async function copyCode() {
  if (!props.script?.code) return
  await navigator.clipboard.writeText(props.script.code)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>
