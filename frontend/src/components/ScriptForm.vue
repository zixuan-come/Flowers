<template>
  <Transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center modal-mask" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl w-[90vw] max-w-[700px] max-h-[85vh] overflow-auto fade-in">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold text-gray-800">{{ isEdit ? '编辑脚本' : '新增脚本' }}</h2>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <form @submit.prevent="submit" class="space-y-4">
            <!-- 标题 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">脚本名称</label>
              <input
                v-model="form.title"
                required
                placeholder="给你的脚本起个名字"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition"
              />
            </div>

            <!-- 语言 + 分类 -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">语言</label>
                <select
                  v-model="form.language"
                  class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition bg-white"
                >
                  <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
                <select
                  v-model="form.category_id"
                  class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition bg-white"
                >
                  <option :value="null">未分类</option>
                  <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">
                    {{ cat.icon }} {{ cat.name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- 描述 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
              <textarea
                v-model="form.description"
                rows="2"
                placeholder="简单描述一下这个脚本的用途"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition resize-none"
              ></textarea>
            </div>

            <!-- 标签 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">标签 <span class="text-gray-400 font-normal">（逗号分隔）</span></label>
              <input
                v-model="form.tags"
                placeholder="如: 爬虫, requests, 自动化"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition"
              />
            </div>

            <!-- 代码 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">代码</label>
              <textarea
                v-model="form.code"
                required
                rows="12"
                placeholder="粘贴你的代码..."
                class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition resize-y font-mono text-sm leading-relaxed"
              ></textarea>
            </div>

            <!-- 提交 -->
            <div class="flex justify-end gap-3 pt-2">
              <button
                type="button"
                @click="$emit('close')"
                class="px-5 py-2.5 text-sm text-gray-600 bg-gray-100 rounded-xl hover:bg-gray-200 transition font-medium"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-5 py-2.5 text-sm text-white bg-gradient-to-r from-flower-400 to-flower-500 rounded-xl hover:from-flower-500 hover:to-flower-600 transition font-medium disabled:opacity-50"
              >
                {{ submitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useStore } from '../stores'
import { createScript, updateScript } from '../api'

const props = defineProps({ show: Boolean, script: Object })
const emit = defineEmits(['close', 'saved'])
const store = useStore()
const submitting = ref(false)

const isEdit = ref(false)
const languages = ['Python', 'JavaScript', 'Shell', 'Bash', 'Go', 'Rust', 'Java', 'SQL', 'HTML', 'CSS', 'TypeScript', 'C', 'C++', 'PHP', 'Ruby', 'Lua', 'Other']

const form = reactive({
  title: '',
  description: '',
  language: 'Python',
  code: '',
  category_id: null,
  tags: ''
})

watch(() => props.show, (val) => {
  if (val && props.script) {
    isEdit.value = true
    Object.assign(form, {
      title: props.script.title,
      description: props.script.description || '',
      language: props.script.language || 'Python',
      code: props.script.code,
      category_id: props.script.category_id,
      tags: props.script.tags || ''
    })
  } else if (val) {
    isEdit.value = false
    Object.assign(form, {
      title: '', description: '', language: 'Python',
      code: '', category_id: null, tags: ''
    })
  }
})

async function submit() {
  if (submitting.value) return
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateScript(props.script.id, { ...form })
    } else {
      await createScript({ ...form })
    }
    emit('saved')
    emit('close')
  } catch (e) {
    alert('保存失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    submitting.value = false
  }
}
</script>
