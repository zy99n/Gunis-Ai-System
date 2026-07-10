<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>ETL流水线管理</span>
          <el-button type="primary" @click="showAddDialog = true">新增流水线</el-button>
        </div>
      </template>

      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="流水线名称">
          <el-input v-model="searchForm.name" placeholder="请输入流水线名称" clearable />
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
        <el-table-column prop="name" label="流水线名称" />
        <el-table-column prop="source_type" label="源类型" width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.source_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_type" label="目标类型" width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.target_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_run_time" label="上次执行" width="180" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button size="small" @click="handleRun(scope.row)">执行</el-button>
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" @click="handleLog(scope.row)">日志</el-button>
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
        <el-form-item label="流水线名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入流水线名称" />
        </el-form-item>
        <el-form-item label="源类型">
          <el-select v-model="formData.source_type" placeholder="请选择源类型">
            <el-option label="MySQL" value="mysql" />
            <el-option label="PostgreSQL" value="postgresql" />
            <el-option label="CSV" value="csv" />
            <el-option label="API" value="api" />
          </el-select>
        </el-form-item>
        <el-form-item label="目标类型">
          <el-select v-model="formData.target_type" placeholder="请选择目标类型">
            <el-option label="MySQL" value="mysql" />
            <el-option label="Elasticsearch" value="elasticsearch" />
            <el-option label="CSV" value="csv" />
            <el-option label="Data Warehouse" value="warehouse" />
          </el-select>
        </el-form-item>
        <el-form-item label="调度方式">
          <el-select v-model="formData.schedule_type" placeholder="请选择调度方式">
            <el-option label="手动" value="manual" />
            <el-option label="定时" value="cron" />
          </el-select>
        </el-form-item>
        <el-form-item label="Cron表达式" v-if="formData.schedule_type === 'cron'">
          <el-input v-model="formData.cron_expression" placeholder="例如: 0 0 * * *" />
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

interface EtlPipeline {
  id: number
  name: string
  source_type: string
  target_type: string
  status: string
  schedule_type: string
  cron_expression: string
  last_run_time: string
  description: string
  created_at: string
}

const tableData = ref<EtlPipeline[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddDialog = ref(false)
const dialogTitle = ref('新增流水线')
const formRef = ref()

const searchForm = reactive({
  name: '',
  status: ''
})

const formData = reactive({
  name: '',
  source_type: '',
  target_type: '',
  schedule_type: 'manual',
  cron_expression: '',
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入流水线名称', trigger: 'blur' }]
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

const handleRun = (row: EtlPipeline) => {
  ElMessage.success(`流水线 "${row.name}" 已开始执行`)
}

const handleEdit = (row: EtlPipeline) => {
  dialogTitle.value = '编辑流水线'
  formData.name = row.name
  formData.source_type = row.source_type
  formData.target_type = row.target_type
  formData.schedule_type = row.schedule_type
  formData.cron_expression = row.cron_expression
  formData.description = row.description
  showAddDialog.value = true
}

const handleLog = (row: EtlPipeline) => {
  ElMessage.info(`查看 "${row.name}" 的执行日志`)
}

const handleDelete = (row: EtlPipeline) => {
  ElMessageBox.confirm('确定要删除该流水线吗？', '提示', {
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
    { id: 1, name: '销售数据同步', source_type: 'MySQL', target_type: 'Elasticsearch', status: 'completed', schedule_type: 'cron', cron_expression: '0 2 * * *', last_run_time: '2024-01-01 02:00:00', description: '', created_at: '2024-01-01 10:00:00' },
    { id: 2, name: '用户数据导出', source_type: 'MySQL', target_type: 'CSV', status: 'pending', schedule_type: 'manual', cron_expression: '', last_run_time: '', description: '', created_at: '2024-01-02 11:00:00' },
    { id: 3, name: 'API数据采集', source_type: 'API', target_type: 'warehouse', status: 'running', schedule_type: 'cron', cron_expression: '*/30 * * * *', last_run_time: '2024-01-03 12:00:00', description: '', created_at: '2024-01-03 12:00:00' }
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