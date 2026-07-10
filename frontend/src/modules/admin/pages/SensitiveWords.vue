<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>敏感词管理</span>
          <el-button type="primary" @click="showAddDialog = true">新增敏感词</el-button>
        </div>
      </template>

      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="敏感词">
          <el-input v-model="searchForm.word" placeholder="请输入敏感词" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="word" label="敏感词" />
        <el-table-column prop="category" label="分类" width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="replace_with" label="替换为" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch v-model="scope.row.status" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
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

    <el-dialog v-model="showAddDialog" :title="dialogTitle" width="400px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="敏感词" prop="word">
          <el-input v-model="formData.word" placeholder="请输入敏感词" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="formData.category" placeholder="请选择分类">
            <el-option label="政治" value="politics" />
            <el-option label="色情" value="pornography" />
            <el-option label="暴力" value="violence" />
            <el-option label="广告" value="advertisement" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="替换为">
          <el-input v-model="formData.replace_with" placeholder="替换内容，留空则删除" />
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

interface SensitiveWord {
  id: number
  word: string
  category: string
  replace_with: string
  status: number
  created_at: string
}

const tableData = ref<SensitiveWord[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddDialog = ref(false)
const dialogTitle = ref('新增敏感词')
const formRef = ref()

const searchForm = reactive({
  word: ''
})

const formData = reactive({
  word: '',
  category: '',
  replace_with: ''
})

const formRules = {
  word: [{ required: true, message: '请输入敏感词', trigger: 'blur' }]
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const resetSearch = () => {
  searchForm.word = ''
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

const handleEdit = (row: SensitiveWord) => {
  dialogTitle.value = '编辑敏感词'
  formData.word = row.word
  formData.category = row.category
  formData.replace_with = row.replace_with
  showAddDialog.value = true
}

const handleDelete = (row: SensitiveWord) => {
  ElMessageBox.confirm('确定要删除该敏感词吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

const handleStatusChange = (row: SensitiveWord) => {
  ElMessage.success(row.status ? '已启用' : '已禁用')
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
    { id: 1, word: '暴力内容', category: '暴力', replace_with: '***', status: 1, created_at: '2024-01-01 10:00:00' },
    { id: 2, word: '色情图片', category: '色情', replace_with: '***', status: 1, created_at: '2024-01-02 11:00:00' },
    { id: 3, word: '政治敏感', category: '政治', replace_with: '***', status: 0, created_at: '2024-01-03 12:00:00' },
    { id: 4, word: '广告推广', category: '广告', replace_with: '', status: 1, created_at: '2024-01-04 13:00:00' }
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