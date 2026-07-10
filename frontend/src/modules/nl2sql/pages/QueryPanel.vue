<template>
  <div class="query-panel">
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card>
          <template #header>
            <h2>智能问数</h2>
          </template>

          <div class="query-input-wrapper">
            <el-input
              v-model="queryInput"
              placeholder="请输入自然语言查询，例如：查询所有用户信息"
              type="textarea"
              :rows="3"
              @keyup.enter="handleQuery"
            />
            <div class="flex justify-end mt-2">
              <el-button type="primary" @click="handleQuery" :loading="loading">
                查询
              </el-button>
            </div>
          </div>

          <div v-if="lastResult" class="mt-4">
            <el-divider>查询结果</el-divider>
            <div v-if="lastResult.is_success">
              <el-alert type="success" :title="`查询成功，耗时 ${lastResult.execution_time_ms}ms`" show-icon />
              <div v-if="lastResult.generated_sql" class="mt-2">
                <el-tag>生成的SQL:</el-tag>
                <pre class="sql-preview">{{ lastResult.generated_sql }}</pre>
              </div>
              <el-table v-if="lastResult.execution_result && lastResult.execution_result.length" :data="lastResult.execution_result" border class="mt-2">
                <el-table-column
                  v-for="(val, key) in lastResult.execution_result[0]"
                  :key="key"
                  :prop="key"
                  :label="key"
                />
              </el-table>
            </div>
            <el-alert v-else type="error" :title="lastResult.error_message" show-icon />
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card>
          <template #header>
            <span>查询历史</span>
          </template>
          <div class="history-list">
            <div
              v-for="item in history"
              :key="item.id"
              class="history-item"
              @click="handleHistoryClick(item)"
            >
              <div class="flex items-center justify-between">
                <span class="text-ellipsis">{{ item.natural_language }}</span>
                <el-icon
                  :class="{ 'favorited': item.is_favorite }"
                  @click.stop="handleFavorite(item.id)"
                >
                  <StarFilled v-if="item.is_favorite" />
                  <Star v-else />
                </el-icon>
              </div>
              <div class="flex items-center justify-between mt-1">
                <el-tag :type="item.is_success ? 'success' : 'danger'" size="small">
                  {{ item.is_success ? '成功' : '失败' }}
                </el-tag>
                <span class="text-sm text-gray">{{ formatTime(item.created_at) }}</span>
              </div>
            </div>
            <div v-if="history.length === 0" class="text-center text-gray py-8">
              暂无查询历史
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { executeQuery, getHistory, toggleFavorite, type QueryResponse, type HistoryResponse } from '@/api/nl2sql'

const queryInput = ref('')
const loading = ref(false)
const lastResult = ref<QueryResponse | null>(null)
const history = ref<HistoryResponse[]>([])

const loadHistory = async () => {
  const res = await getHistory({ limit: 20 })
  history.value = res
}

const handleQuery = async () => {
  if (!queryInput.value.trim()) {
    ElMessage.warning('请输入查询内容')
    return
  }

  loading.value = true
  try {
    const res = await executeQuery({ natural_language: queryInput.value })
    lastResult.value = res
    await loadHistory()
  } catch (error) {
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

const handleHistoryClick = (item: HistoryResponse) => {
  queryInput.value = item.natural_language
}

const handleFavorite = async (id: number) => {
  try {
    const res = await toggleFavorite(id)
    const index = history.value.findIndex(h => h.id === id)
    if (index !== -1) {
      history.value[index].is_favorite = res.is_favorite
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const formatTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(loadHistory)
</script>

<style scoped>
.query-input-wrapper {
  width: 100%;
}

.mt-2 {
  margin-top: 8px;
}

.mt-4 {
  margin-top: 16px;
}

.sql-preview {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  font-family: monospace;
  overflow-x: auto;
  margin-top: 8px;
}

.history-list {
  max-height: 500px;
  overflow-y: auto;
}

.history-item {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: #f5f7fa;
}

.history-item:last-child {
  border-bottom: none;
}

.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.text-sm {
  font-size: 12px;
}

.text-gray {
  color: #909399;
}

.favorited {
  color: #e6a23c;
}
</style>