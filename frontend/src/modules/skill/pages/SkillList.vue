<template>
  <div class="skill-list">
    <el-card>
      <template #header>
        <div class="flex items-center justify-between">
          <h2>AI技能管理</h2>
          <div class="flex gap-2">
            <el-button type="primary" @click="showAddDialog">新增技能</el-button>
            <el-button type="success" @click="showGenerateDialog">AI生成技能</el-button>
          </div>
        </div>
      </template>

      <el-table :data="skills" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="技能名称" />
        <el-table-column prop="code" label="技能编码" width="120" />
        <el-table-column prop="category" label="分类" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.category">{{ row.category }}</el-tag>
            <span v-else class="text-gray">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" @click="handleTest(row.id)">测试</el-button>
            <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="handleToggle(row.id)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="技能名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入技能名称" />
        </el-form-item>
        <el-form-item label="技能编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入技能编码" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="formData.category" placeholder="请输入分类" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入技能描述" />
        </el-form-item>
        <el-form-item label="提示词模板" prop="prompt_template">
          <el-input v-model="formData.prompt_template" type="textarea" :rows="4" placeholder="请输入提示词模板" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="formData.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="generateVisible" title="AI生成技能" width="500px">
      <el-form ref="generateFormRef" :model="generateData" :rules="generateRules" label-width="100px">
        <el-form-item label="技能名称" prop="name">
          <el-input v-model="generateData.name" placeholder="请输入技能名称" />
        </el-form-item>
        <el-form-item label="技能描述" prop="description">
          <el-input v-model="generateData.description" type="textarea" placeholder="请输入技能描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="generateVisible = false">取消</el-button>
        <el-button type="success" @click="handleGenerate">生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSkills, createSkill, updateSkill, deleteSkill, aiGenerateSkill, testSkill, toggleSkill, type AiSkill, type SkillCreate, type SkillGenerateRequest } from '@/api/skill'

const skills = ref<AiSkill[]>([])
const dialogVisible = ref(false)
const generateVisible = ref(false)
const dialogTitle = ref('新增技能')
const formRef = ref()
const generateFormRef = ref()
const editingId = ref<number | null>(null)

const formData = ref<SkillCreate>({
  name: '',
  code: '',
  description: '',
  prompt_template: '',
  sort_order: 0,
  is_active: true
})

const generateData = ref<SkillGenerateRequest>({
  name: '',
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入技能名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入技能编码', trigger: 'blur' }],
  prompt_template: [{ required: true, message: '请输入提示词模板', trigger: 'blur' }]
}

const generateRules = {
  name: [{ required: true, message: '请输入技能名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入技能描述', trigger: 'blur' }]
}

const loadData = async () => {
  const res = await getSkills()
  skills.value = res
}

const showAddDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增技能'
  formData.value = {
    name: '',
    code: '',
    description: '',
    prompt_template: '',
    sort_order: 0,
    is_active: true
  }
  dialogVisible.value = true
}

const showEditDialog = (row: AiSkill) => {
  editingId.value = row.id
  dialogTitle.value = '编辑技能'
  formData.value = {
    name: row.name,
    code: row.code,
    description: row.description ?? '',
    prompt_template: row.prompt_template,
    sort_order: row.sort_order,
    is_active: row.is_active
  }
  dialogVisible.value = true
}

const showGenerateDialog = () => {
  generateData.value = {
    name: '',
    description: ''
  }
  generateVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (!valid) return

  try {
    if (editingId.value) {
      await updateSkill(editingId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createSkill(formData.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleGenerate = async () => {
  if (!generateFormRef.value) return
  const valid = await generateFormRef.value.validate()
  if (!valid) return

  try {
    await aiGenerateSkill(generateData.value)
    ElMessage.success('生成成功')
    generateVisible.value = false
    await loadData()
  } catch (error) {
    ElMessage.error('生成失败')
  }
}

const handleTest = async (id: number) => {
  try {
    const res = await testSkill(id)
    if (res.success) {
      ElMessage.success(res.message)
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    ElMessage.error('测试失败')
  }
}

const handleToggle = async (id: number) => {
  try {
    await toggleSkill(id)
    ElMessage.success('状态已切换')
    await loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该技能吗？', '提示', { type: 'warning' })
    await deleteSkill(id)
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
.text-gray {
  color: #909399;
}
</style>