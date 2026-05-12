<template>
  <Transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center modal-mask" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl w-[90vw] max-w-[500px] max-h-[70vh] overflow-auto fade-in">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold text-gray-800">管理分类</h2>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- 新增分类 -->
          <div class="flex gap-2 mb-4">
            <input
              v-model="newName"
              placeholder="新分类名称"
              class="flex-1 px-3 py-2 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition text-sm"
            />
            <input
              v-model="newIcon"
              placeholder="图标"
              class="w-16 px-3 py-2 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition text-sm text-center"
            />
            <button
              @click="addCategory"
              class="px-4 py-2 bg-gradient-to-r from-flower-400 to-flower-500 text-white rounded-xl text-sm font-medium hover:from-flower-500 hover:to-flower-600 transition"
            >
              添加
            </button>
          </div>

          <!-- 分类列表 -->
          <div class="space-y-2">
            <div
              v-for="cat in store.categories"
              :key="cat.id"
              class="flex items-center gap-3 p-3 rounded-xl bg-gray-50 group"
            >
              <span v-if="editingId !== cat.id" class="text-lg">{{ cat.icon }}</span>
              <input
                v-else
                v-model="editIcon"
                class="w-10 text-center text-lg bg-white rounded-lg border border-gray-200 py-0.5"
              />

              <span v-if="editingId !== cat.id" class="flex-1 text-sm text-gray-700">{{ cat.name }}</span>
              <input
                v-else
                v-model="editName"
                class="flex-1 text-sm px-2 py-1 bg-white rounded-lg border border-gray-200"
              />

              <div class="flex gap-1.5 opacity-0 group-hover:opacity-100 transition">
                <template v-if="editingId !== cat.id">
                  <button @click="startEdit(cat)" class="text-xs px-2.5 py-1 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition">
                    编辑
                  </button>
                  <button @click="removeCategory(cat.id)" class="text-xs px-2.5 py-1 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition">
                    删除
                  </button>
                </template>
                <template v-else>
                  <button @click="saveEdit(cat.id)" class="text-xs px-2.5 py-1 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition">
                    保存
                  </button>
                  <button @click="editingId = null" class="text-xs px-2.5 py-1 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition">
                    取消
                  </button>
                </template>
              </div>
            </div>

            <p v-if="store.categories.length === 0" class="text-center text-gray-400 text-sm py-4">
              暂无分类
            </p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from '../stores'
import { createCategory, updateCategory, deleteCategory } from '../api'

defineProps({ show: Boolean })
const emit = defineEmits(['close', 'updated'])
const store = useStore()

const newName = ref('')
const newIcon = ref('📁')
const editingId = ref(null)
const editName = ref('')
const editIcon = ref('')

async function addCategory() {
  if (!newName.value.trim()) return
  try {
    await createCategory({ name: newName.value.trim(), icon: newIcon.value || '📁' })
    newName.value = ''
    newIcon.value = '📁'
    emit('updated')
  } catch (e) {
    alert('添加失败: ' + (e.response?.data?.detail || e.message))
  }
}

function startEdit(cat) {
  editingId.value = cat.id
  editName.value = cat.name
  editIcon.value = cat.icon
}

async function saveEdit(id) {
  try {
    await updateCategory(id, { name: editName.value.trim(), icon: editIcon.value || '📁' })
    editingId.value = null
    emit('updated')
  } catch (e) {
    alert('保存失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function removeCategory(id) {
  if (!confirm('确认删除此分类？该分类下的脚本将变为"未分类"')) return
  try {
    await deleteCategory(id)
    emit('updated')
  } catch (e) {
    alert('删除失败: ' + (e.response?.data?.detail || e.message))
  }
}
</script>
