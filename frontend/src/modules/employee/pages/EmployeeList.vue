<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>数字员工管理</span>
          <el-button type="primary" @click="showAddDialog = true">新增员工</el-button>
        </div>
      </template>

      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="员工名称">
          <el-input v-model="searchForm.name" placeholder="请输入员工名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable>
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="员工名称" />
        <el-table-column prop="avatar" label="头像" width="100">
          <template #default="scope">
            <el-avatar :src="scope.row.avatar" />
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch v-model="scope.row.status" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" @click="handleChat(scope.row)">聊天</el-button>
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

    <el-dialog v-model="showAddDialog" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="员工名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入员工名称" />
        </el-form-item>
        <el-form-item label="头像">
          <el-input v-model="formData.avatar" placeholder="请输入头像URL" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="formData.role" placeholder="请选择角色">
            <el-option label="客服" value="customer_service" />
            <el-option label="助手" value="assistant" />
            <el-option label="分析师" value="analyst" />
          </el-select>
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

interface Employee {
  id: number
  name: string
  avatar: string
  description: string
  status: number
  role: string
  created_at: string
}

const tableData = ref<Employee[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddDialog = ref(false)
const dialogTitle = ref('新增员工')
const formRef = ref()

const searchForm = reactive({
  name: '',
  status: ''
})

const formData = reactive({
  name: '',
  avatar: '',
  description: '',
  role: ''
})

const formRules = {
  name: [{ required: true, message: '请输入员工名称', trigger: 'blur' }]
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

const handleAdd = () => {
  dialogTitle.value = '新增员工'
  formData.name = ''
  formData.avatar = ''
  formData.description = ''
  formData.role = ''
  showAddDialog.value = true
}

const handleEdit = (row: Employee) => {
  dialogTitle.value = '编辑员工'
  formData.name = row.name
  formData.avatar = row.avatar
  formData.description = row.description
  formData.role = row.role
  showAddDialog.value = true
}

const handleDelete = (row: Employee) => {
  ElMessageBox.confirm('确定要删除该员工吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

const handleStatusChange = (row: Employee) => {
  ElMessage.success(row.status ? '已启用' : '已禁用')
}

const handleChat = (row: Employee) => {
  ElMessage.info(`与${row.name}聊天功能开发中`)
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
    { id: 1, name: '智能客服小美', avatar: '', description: '专业的客服助手', status: 1, role: 'customer_service', created_at: '2024-01-01 10:00:00' },
    { id: 2, name: '数据分析助手', avatar: '', description: '数据分析专家', status: 1, role: 'analyst', created_at: '2024-01-02 11:00:00' },
    { id: 3, name: '办公小助手', avatar: '', description: '日常办公助手', status: 0, role: 'assistant', created_at: '2024-01-03 12:00:00' }
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