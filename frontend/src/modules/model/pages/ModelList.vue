<template>
  <div class="model-list">
    <el-card>
      <template #header>
        <div class="flex items-center justify-between">
          <h2>AI模型管理</h2>
          <el-button type="primary" @click="showAddDialog">新增模型</el-button>
        </div>
      </template>

      <el-table :data="models" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="模型名称" />
        <el-table-column prop="model_type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.model_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="model_name" label="模型标识" />
        <el-table-column prop="api_base" label="API地址" width="300" />
        <el-table-column prop="temperature" label="温度" width="80" />
        <el-table-column prop="max_tokens" label="最大Token" width="100" />
        <el-table-column prop="is_default" label="默认" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success">默认</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template #default="{ row }">
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" @click="handleTest(row.id)">测试连通性</el-button>
            <el-button size="small" :type="row.is_default ? 'info' : 'primary'" @click="handleSetDefault(row.id)" :disabled="row.is_default">
              {{ row.is_default ? '已默认' : '设为默认' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="formData.model_type" placeholder="请选择模型类型">
            <el-option label="OpenAI" value="openai" />
            <el-option label="Anthropic" value="anthropic" />
            <el-option label="Google" value="google" />
            <el-option label="百度" value="baidu" />
            <el-option label="阿里云" value="aliyun" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="API基础地址" prop="api_base">
          <el-input v-model="formData.api_base" placeholder="请输入API基础地址" />
        </el-form-item>
        <el-form-item label="API密钥" prop="api_key">
          <el-input v-model="formData.api_key" type="password" placeholder="请输入API密钥" show-password />
        </el-form-item>
        <el-form-item label="模型标识" prop="model_name">
          <el-input v-model="formData.model_name" placeholder="请输入模型标识" />
        </el-form-item>
        <el-form-item label="温度参数" prop="temperature">
          <el-slider v-model="formData.temperature" :min="0" :max="2" :step="0.1" :show-input="true" />
        </el-form-item>
        <el-form-item label="最大Token" prop="max_tokens">
          <el-input-number v-model="formData.max_tokens" :min="100" :max="10000" />
        </el-form-item>
        <el-form-item label="超时时间" prop="timeout">
          <el-input-number v-model="formData.timeout" :min="5" :max="300" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="formData.is_default" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getModels, createModel, updateModel, deleteModel, setDefaultModel, testModel, type AiModel, type AiModelCreate } from '@/api/model'

const models = ref<AiModel[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增模型')
const formRef = ref()
const editingId = ref<number | null>(null)

const typeLabels: Record<string, string> = {
  openai: 'OpenAI',
  anthropic: 'Anthropic',
  google: 'Google',
  baidu: '百度',
  aliyun: '阿里云',
  custom: '自定义'
}

const getTypeLabel = (type: string) => typeLabels[type] || type

const formData = ref<AiModelCreate>({
  name: '',
  model_type: 'openai',
  api_base: '',
  api_key: '',
  model_name: '',
  temperature: 0.7,
  max_tokens: 2000,
  timeout: 30,
  is_default: false,
  is_active: true,
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  model_type: [{ required: true, message: '请选择模型类型', trigger: 'change' }],
  api_key: [{ required: true, message: '请输入API密钥', trigger: 'blur' }],
  model_name: [{ required: true, message: '请输入模型标识', trigger: 'blur' }]
}

const loadData = async () => {
  const res = await getModels()
  models.value = res
}

const showAddDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增模型'
  formData.value = {
    name: '',
    model_type: 'openai',
    api_base: '',
    api_key: '',
    model_name: '',
    temperature: 0.7,
    max_tokens: 2000,
    timeout: 30,
    is_default: false,
    is_active: true,
    description: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (row: AiModel) => {
  editingId.value = row.id
  dialogTitle.value = '编辑模型'
  formData.value = {
    name: row.name,
    model_type: row.model_type,
    api_base: row.api_base ?? '',
    api_key: row.api_key,
    model_name: row.model_name,
    temperature: row.temperature,
    max_tokens: row.max_tokens,
    timeout: row.timeout,
    is_default: row.is_default,
    is_active: row.is_active,
    description: row.description ?? ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (!valid) return

  try {
    if (editingId.value) {
      await updateModel(editingId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createModel(formData.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleTest = async (id: number) => {
  try {
    const res = await testModel(id)
    if (res.success) {
      ElMessage.success(res.message)
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    ElMessage.error('测试失败')
  }
}

const handleSetDefault = async (id: number) => {
  try {
    await setDefaultModel(id)
    ElMessage.success('已设为默认模型')
    await loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该模型吗？', '提示', { type: 'warning' })
    await deleteModel(id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(loadData)
</script>

<style scoped>
</style>