<template>
  <div class="chat-container">
    <el-row :gutter="0">
      <el-col :span="6" class="chat-sidebar">
        <div class="sidebar-header">
          <h3>消息列表</h3>
          <el-input placeholder="搜索" class="search-input" />
        </div>
        <div class="conversation-list">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: currentConversation?.id === conv.id }"
            @click="selectConversation(conv)"
          >
            <el-avatar :size="48" :src="conv.avatar" />
            <div class="conv-info">
              <div class="conv-name">{{ conv.name }}</div>
              <div class="conv-preview">{{ conv.last_message }}</div>
            </div>
            <div class="conv-meta">
              <div class="conv-time">{{ conv.time }}</div>
              <el-badge v-if="conv.unread > 0" :value="conv.unread" class="unread-badge" />
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="18" class="chat-main">
        <div v-if="!currentConversation" class="empty-state">
          <el-icon size="64" color="#ccc"><Message /></el-icon>
          <p>请选择一个会话开始聊天</p>
        </div>

        <div v-else class="chat-area">
          <div class="chat-header">
            <el-avatar :size="40" :src="currentConversation.avatar" />
            <div class="header-info">
              <div class="header-name">{{ currentConversation.name }}</div>
              <div class="header-status">
                <span class="online-dot"></span>在线
              </div>
            </div>
            <div class="header-actions">
              <el-button type="text">
                <el-icon><Phone /></el-icon>
              </el-button>
              <el-button type="text">
                <el-icon><VideoCamera /></el-icon>
              </el-button>
              <el-button type="text">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="message-list" ref="messageList">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message-item"
              :class="{ self: msg.is_self }"
            >
              <el-avatar :size="40" :src="msg.is_self ? '' : currentConversation.avatar" />
              <div class="message-content">
                <div class="message-bubble">{{ msg.content }}</div>
                <div class="message-time">{{ msg.time }}</div>
              </div>
            </div>
          </div>

          <div class="chat-footer">
            <el-button type="text">
              <el-icon><Plus /></el-icon>
            </el-button>
            <el-input
              v-model="inputMessage"
              placeholder="输入消息..."
              @keyup.enter="sendMessage"
            />
            <el-button type="primary" @click="sendMessage">发送</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { Message, Phone, VideoCamera, MoreFilled, Plus } from '@element-plus/icons-vue'

interface Conversation {
  id: number
  name: string
  avatar: string
  last_message: string
  time: string
  unread: number
}

interface MessageItem {
  id: number
  content: string
  time: string
  is_self: boolean
}

const conversations = ref<Conversation[]>([])
const currentConversation = ref<Conversation | null>(null)
const messages = ref<MessageItem[]>([])
const inputMessage = ref('')
const messageList = ref()

const selectConversation = (conv: Conversation) => {
  currentConversation.value = conv
  loadMessages()
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  
  const newMessage: MessageItem = {
    id: Date.now(),
    content: inputMessage.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    is_self: true
  }
  
  messages.value.push(newMessage)
  inputMessage.value = ''
  
  nextTick(() => {
    if (messageList.value) {
      messageList.value.scrollTop = messageList.value.scrollHeight
    }
  })
  
  setTimeout(() => {
    const reply: MessageItem = {
      id: Date.now() + 1,
      content: '收到，我会尽快处理！',
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      is_self: false
    }
    messages.value.push(reply)
    nextTick(() => {
      if (messageList.value) {
        messageList.value.scrollTop = messageList.value.scrollHeight
      }
    })
  }, 1000)
}

const loadMessages = () => {
  messages.value = [
    { id: 1, content: '你好！有什么可以帮你的吗？', time: '10:00', is_self: false },
    { id: 2, content: '我想查询一下销售数据', time: '10:01', is_self: true },
    { id: 3, content: '好的，我帮你查询一下...', time: '10:02', is_self: false },
    { id: 4, content: '上周的销售额是100万', time: '10:03', is_self: false }
  ]
  
  nextTick(() => {
    if (messageList.value) {
      messageList.value.scrollTop = messageList.value.scrollHeight
    }
  })
}

const loadConversations = () => {
  conversations.value = [
    { id: 1, name: '智能客服小美', avatar: '', last_message: '收到，我会尽快处理！', time: '10:30', unread: 2 },
    { id: 2, name: '数据分析助手', avatar: '', last_message: '已完成数据分析报告', time: '09:15', unread: 0 },
    { id: 3, name: '张三', avatar: '', last_message: '会议几点开始？', time: '昨天', unread: 1 },
    { id: 4, name: '李四', avatar: '', last_message: '文件已发送', time: '周一', unread: 0 }
  ]
  
  if (conversations.value.length > 0) {
    currentConversation.value = conversations.value[0]
    loadMessages()
  }
}

onMounted(() => {
  loadConversations()
})
</script>

<style scoped>
.chat-container {
  height: 100%;
  display: flex;
}

.chat-sidebar {
  height: 100%;
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
}

.search-input {
  width: 100%;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background-color: #e8e8e8;
}

.conversation-item.active {
  background-color: #fff;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.conv-preview {
  font-size: 12px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-meta {
  text-align: right;
}

.conv-time {
  font-size: 12px;
  color: #999;
}

.unread-badge {
  margin-top: 4px;
}

.chat-main {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.empty-state p {
  margin-top: 16px;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 12px 16px;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-info {
  flex: 1;
}

.header-name {
  font-weight: 500;
}

.header-status {
  font-size: 12px;
  color: #67c23a;
}

.online-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #67c23a;
  margin-right: 4px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #fafafa;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message-item.self {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 70%;
}

.message-item.self .message-content {
  text-align: right;
}

.message-bubble {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-item.self .message-bubble {
  background-color: #409eff;
  color: #fff;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.chat-footer {
  padding: 12px 16px;
  background-color: #fff;
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-footer .el-input {
  flex: 1;
}
</style>