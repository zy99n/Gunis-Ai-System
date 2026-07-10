import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const savedUserInfo = localStorage.getItem('user_info')
  const userInfo = ref<UserInfo | null>(
    savedUserInfo ? JSON.parse(savedUserInfo) : null
  )

  const isLoggedIn = computed(() => {
    return !!token.value && !!userInfo.value
  })

  const isAdmin = computed(() => {
    return userInfo.value?.is_admin ?? false
  })

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    localStorage.setItem('user_info', JSON.stringify(info))
  }

  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
  }

  // 从localStorage恢复用户信息
  const restoreUserInfo = () => {
    const savedUserInfo = localStorage.getItem('user_info')
    if (savedUserInfo) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
      } catch {
        userInfo.value = null
      }
    }
  }

  return {
    userInfo,
    token,
    isLoggedIn,
    isAdmin,
    setToken,
    setUserInfo,
    logout,
    restoreUserInfo
  }
})