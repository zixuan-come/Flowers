<template>
  <Transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center modal-mask" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-[360px] fade-in">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">🔐</div>
          <h3 class="text-lg font-semibold text-gray-800">需要管理权限</h3>
          <p class="text-sm text-gray-500 mt-1">请输入管理密码</p>
        </div>
        <input
          ref="inputRef"
          v-model="password"
          type="password"
          placeholder="输入密码..."
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-flower-400 focus:ring-2 focus:ring-flower-200 outline-none transition text-center text-lg tracking-widest"
          @keyup.enter="submit"
        />
        <p v-if="error" class="text-red-500 text-sm text-center mt-2">密码错误，请重试</p>
        <button
          @click="submit"
          :disabled="submitting"
          class="w-full mt-4 py-3 bg-gradient-to-r from-flower-400 to-flower-500 text-white rounded-xl font-medium hover:from-flower-500 hover:to-flower-600 transition disabled:opacity-50"
        >
          {{ submitting ? '验证中...' : '确认' }}
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useStore } from '../stores'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close', 'success'])
const store = useStore()

const password = ref('')
const error = ref(false)
const submitting = ref(false)
const inputRef = ref(null)

watch(() => props.show, (val) => {
  if (val) {
    password.value = ''
    error.value = false
    nextTick(() => inputRef.value?.focus())
  }
})

async function submit() {
  if (!password.value.trim() || submitting.value) return
  submitting.value = true
  error.value = false
  const ok = await store.checkPassword(password.value)
  submitting.value = false
  if (ok) {
    emit('success')
    emit('close')
  } else {
    error.value = true
  }
}
</script>
