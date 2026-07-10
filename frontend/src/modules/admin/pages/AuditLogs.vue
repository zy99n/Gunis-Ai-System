<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>审计日志</span>
          <el-button type="primary" @click="handleExport">导出日志</el-button>
        </div>
      </template>

      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="操作人">
          <el-input v-model="searchForm.user_name" placeholder="请输入操作人" clearable />
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="searchForm.action_type" placeholder="全部" clearable>
            <el-option label="登录" value="login" />
            <el-option label="创建" value="create" />
            <el-option label="更新" value="update" />
            <el-option label="删除" value="delete" />
            <el-option label="查询" value="query" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="searchForm.date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_name" label="操作人" />
        <el-table-column prop="action_type" label="操作类型" width="100">
          <template #default="scope">
            <el-tag :type="getActionTag(scope.row.action_type)">
              {{ getActionText(scope.row.action_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="resource" label="操作资源" />
        <el-table-column prop="detail" label="操作详情" />
        <el-table-column prop="ip_address" label="IP地址" width="150" />
        <el-table-column prop="user_agent" label="用户代理" width="200" />
        <el-table-column prop="created_at" label="操作时间" width="180" />
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

interface AuditLog {
  id: number
  user_name: string
  action_type: string
  resource: string
  detail: string
  ip_address: string
  user_agent: string
  created_at: string
}

const tableData = ref<AuditLog[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const searchForm = reactive({
  user_name: '',
  action_type: '',
  date_range: [] as string[]
})

const getActionTag = (type: string) => {
  const tags: Record<string, string> = {
    login: 'info',
    create: 'success',
    update: 'warning',
    delete: 'danger',
    query: ''
  }
  return tags[type] || ''
}

const getActionText = (type: string) => {
  const texts: Record<string, string> = {
    login: '登录',
    create: '创建',
    update: '更新',
    delete: '删除',
    query: '查询'
  }
  return texts[type] || type
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const resetSearch = () => {
  searchForm.user_name = ''
  searchForm.action_type = ''
  searchForm.date_range = []
  currentPage.value = 1
  loadData()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadData()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadData()
}

const handleExport = () => {
  ElMessage.success('日志导出功能开发中')
}

const loadData = () => {
  tableData.value = [
    { id: 1, user_name: 'admin', action_type: 'login', resource: '系统', detail: '用户登录成功', ip_address: '192.168.1.100', user_agent: 'Mozilla/5.0', created_at: '2024-01-01 10:00:00' },
    { id: 2, user_name: 'admin', action_type: 'create', resource: '部门', detail: '创建部门：技术部', ip_address: '192.168.1.100', user_agent: 'Mozilla/5.0', created_at: '2024-01-01 10:05:00' },
    { id: 3, user_name: 'user1', action_type: 'query', resource: '数据', detail: '查询销售数据', ip_address: '192.168.1.101', user_agent: 'Mozilla/5.0', created_at: '2024-01-01 11:00:00' },
    { id: 4, user_name: 'admin', action_type: 'update', resource: '模型', detail: '更新模型配置', ip_address: '192.168.1.100', user_agent: 'Mozilla/5.0', created_at: '2024-01-01 12:00:00' },
    { id: 5, user_name: 'user2', action_type: 'delete', resource: '技能', detail: '删除技能：测试技能', ip_address: '192.168.1.102', user_agent: 'Mozilla/5.0', created_at: '2024-01-02 09:00:00' }
  ]
  total.value = tableData.value.length
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container {
  min-height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>