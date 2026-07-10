<template>
  <div class="department-manage">
    <el-card>
      <template #header>
        <div class="flex items-center justify-between">
          <h2>部门管理</h2>
          <el-button type="primary" @click="showAddDialog">新增部门</el-button>
        </div>
      </template>
      
      <el-tree
        ref="treeRef"
        :data="departments"
        :props="defaultProps"
        node-key="id"
        :expand-on-click-node="false"
        class="tree-container"
      >
        <template #default="{ node, data }">
          <span class="flex items-center justify-between w-full">
            <span>{{ node.label }}</span>
            <span class="actions">
              <el-button size="small" @click="showEditDialog(data)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(data.id)">删除</el-button>
            </span>
          </span>
        </template>
      </el-tree>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent_id">
          <el-select v-model="formData.parent_id" placeholder="请选择上级部门" clearable>
            <el-option label="无（顶级部门）" :value="null" />
            <template v-for="dept in departments" :key="dept.id">
              <el-option :label="dept.name" :value="dept.id" />
              <template v-for="child in dept.children" :key="child.id">
                <el-option :label="'  └ ' + child.name" :value="child.id" />
              </template>
            </template>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="formData.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入部门描述" />
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
import { getDepartmentTree, createDepartment, updateDepartment, deleteDepartment, type Department, type DepartmentCreate } from '@/api/organization'

const treeRef = ref()
const departments = ref<Department[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增部门')
const formRef = ref()
const editingId = ref<number | null>(null)

const defaultProps = {
  children: 'children',
  label: 'name'
}

const formData = ref<DepartmentCreate>({
  name: '',
  parent_id: null,
  sort_order: 0,
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }]
}

const loadData = async () => {
  const res = await getDepartmentTree()
  departments.value = res
}

const showAddDialog = () => {
  editingId.value = null
  dialogTitle.value = '新增部门'
  formData.value = {
    name: '',
    parent_id: null,
    sort_order: 0,
    description: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (data: Department) => {
  editingId.value = data.id
  dialogTitle.value = '编辑部门'
  formData.value = {
    name: data.name,
    parent_id: data.parent_id,
    sort_order: data.sort_order,
    description: data.description ?? ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (!valid) return

  try {
    if (editingId.value) {
      await updateDepartment(editingId.value, formData.value)
      ElMessage.success('更新成功')
    } else {
      await createDepartment(formData.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该部门吗？', '提示', { type: 'warning' })
    await deleteDepartment(id)
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
.tree-container {
  max-height: 600px;
  overflow-y: auto;
}

.actions {
  display: flex;
  gap: 8px;
}

.actions :deep(.el-button) {
  margin: 0;
}
</style>