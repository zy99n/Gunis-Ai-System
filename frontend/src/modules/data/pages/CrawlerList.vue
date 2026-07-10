<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>爬虫任务管理</span>
          <el-button type="primary" @click="showAddDialog = true">新增任务</el-button>
        </div>
      </template>

      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="任务名称">
          <el-input v-model="searchForm.name" placeholder="请输入任务名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable>
            <el-option label="待执行" value="pending" />
            <el-option label="执行中" value="running" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="url" label="目标URL" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="crawled_count" label="已爬取" width="100" />
        <el-table-column prop="total_count" label="总数" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button size="small" @click="handleStart(scope.row)">启动</el-button>
            <el-button size="small" @click="handleStop(scope.row)">停止</el-button>
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
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

    <el-dialog v-model="showAddDialog" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="目标URL" prop="url">
          <el-input v-model="formData.url" placeholder="请输入目标URL" />
        </el-form-item>
        <el-form-item label="爬取深度">
          <el-input-number v-model="formData.depth" :min="1" :max="10" />
        </el-form-item>
        <el-form-item label="最大数量">
          <el-input-number v-model="formData.max_count" :min="1" :max="10000" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

interface CrawlerTask {
  id: number
  name: string
  url: string
  status: string
  depth: number
  max_count: number
  crawled_count: number
  total_count: number
  description: string
  created_at: string
  updated_at: string
}

const tableData = ref<CrawlerTask[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddDialog = ref(false)
const dialogTitle = ref('新增任务')
const formRef = ref()

const searchForm = reactive({
  name: '',
  status: ''
})

const formData = reactive({
  name: '',
  url: '',
  depth: 3,
  max_count: 100,
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  url: [{ required: true, message: '请输入目标URL', trigger: 'blur' }]
}

const getStatusTag = (status: string) => {
  const tags: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return tags[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待执行',
    running: '执行中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.status = ''
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

const handleStart = (row: CrawlerTask) => {
  ElMessage.success(`任务 "${row.name}" 已启动`)
}

const handleStop = (row: CrawlerTask) => {
  ElMessage.success(`任务 "${row.name}" 已停止`)
}

const handleEdit = (row: CrawlerTask) => {
  dialogTitle.value = '编辑任务'
  formData.name = row.name
  formData.url = row.url
  formData.depth = row.depth
  formData.max_count = row.max_count
  formData.description = row.description
  showAddDialog.value = true
}

const handleDelete = (row: CrawlerTask) => {
  ElMessageBox.confirm('确定要删除该任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  showAddDialog.value = false
  ElMessage.success('操作成功')
  loadData()
}

const loadData = () => {
  tableData.value = [
    { id: 1, name: '新闻网站爬取', url: 'https://news.example.com', status: 'running', depth: 3, max_count: 100, crawled_count: 45, total_count: 100, description: '', created_at: '2024-01-01 10:00:00', updated_at: '2024-01-01 10:30:00' },
    { id: 2, name: '商品数据采集', url: 'https://shop.example.com', status: 'completed', depth: 2, max_count: 50, crawled_count: 50, total_count: 50, description: '', created_at: '2024-01-02 11:00:00', updated_at: '2024-01-02 12:00:00' },
    { id: 3, name: '博客文章抓取', url: 'https://blog.example.com', status: 'pending', depth: 5, max_count: 200, crawled_count: 0, total_count: 0, description: '', created_at: '2024-01-03 12:00:00', updated_at: '2024-01-03 12:00:00' }
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