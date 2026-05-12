<template>
  <div
    class="bg-white/80 backdrop-blur-sm rounded-2xl overflow-hidden card-hover cursor-pointer border border-white/50"
    @click="$emit('click', script)"
  >
    <!-- 顶部色条 -->
    <div class="h-1.5 bg-gradient-to-r" :class="gradientClass"></div>

    <div class="p-5">
      <!-- 标题行 -->
      <div class="flex items-start justify-between mb-3">
        <h3 class="font-semibold text-gray-800 text-base leading-snug line-clamp-2 flex-1 mr-2">
          {{ script.title }}
        </h3>
        <span
          class="text-xs px-2.5 py-1 rounded-full font-mono font-medium shrink-0"
          :class="`lang-${script.language?.toLowerCase() || 'default'}`"
        >
          {{ script.language || 'text' }}
        </span>
      </div>

      <!-- 描述 -->
      <p class="text-gray-500 text-sm leading-relaxed line-clamp-2 mb-4">
        {{ script.description || '暂无描述' }}
      </p>

      <!-- 底部信息 -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm">{{ categoryIcon }}</span>
          <span class="text-xs text-gray-400">{{ categoryName }}</span>
        </div>
        <span class="text-xs text-gray-400">{{ formatDate(script.created_at) }}</span>
      </div>

      <!-- 标签 -->
      <div v-if="script.tags" class="flex flex-wrap gap-1.5 mt-3">
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
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from '../stores'

const props = defineProps({ script: Object })
defineEmits(['click'])
const store = useStore()

const categoryName = computed(() => store.getCategoryName(props.script.category_id))
const categoryIcon = computed(() => store.getCategoryIcon(props.script.category_id))

const tagList = computed(() => {
  if (!props.script.tags) return []
  return props.script.tags.split(',').map(t => t.trim()).filter(Boolean)
})

const gradients = [
  'from-pink-300 to-purple-300',
  'from-blue-300 to-cyan-300',
  'from-green-300 to-emerald-300',
  'from-orange-300 to-yellow-300',
  'from-violet-300 to-fuchsia-300',
  'from-teal-300 to-sky-300'
]
const gradientClass = computed(() => gradients[props.script.id % gradients.length])

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>
