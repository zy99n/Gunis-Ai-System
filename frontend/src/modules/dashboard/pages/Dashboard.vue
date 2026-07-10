<template>
  <div class="dashboard">
    <el-card class="welcome-card">
      <h2>👋 欢迎使用企业智能协同平台</h2>
      <p>当前用户：{{ userInfo?.nickname || userInfo?.username }}</p>
    </el-card>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">12</div>
            <div class="stat-label">组织成员</div>
          </div>
          <el-icon class="stat-icon" color="#409EFF"><User /></el-icon>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">5</div>
            <div class="stat-label">AI模型</div>
          </div>
          <el-icon class="stat-icon" color="#67C23A"><Box /></el-icon>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">8</div>
            <div class="stat-label">AI技能</div>
          </div>
          <el-icon class="stat-icon" color="#E6A23C"><Tools /></el-icon>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">3</div>
            <div class="stat-label">数字员工</div>
          </div>
          <el-icon class="stat-icon" color="#F56C6C"><Avatar /></el-icon>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :md="16">
        <el-card class="function-card">
          <template #header>
            <div class="card-header">
              <span>功能模块概览</span>
            </div>
          </template>
          <div class="function-grid">
            <div class="function-item" @click="goTo('/organization/department')">
              <el-icon size="40" color="#409EFF"><OfficeBuilding /></el-icon>
              <div class="function-name">组织管理</div>
              <div class="function-desc">管理部门和用户</div>
            </div>
            <div class="function-item" @click="goTo('/model/list')">
              <el-icon size="40" color="#67C23A"><Box /></el-icon>
              <div class="function-name">模型管理</div>
              <div class="function-desc">配置AI模型</div>
            </div>
            <div class="function-item" @click="goTo('/nl2sql/query')">
              <el-icon size="40" color="#9B59B6"><MagicStick /></el-icon>
              <div class="function-name">智能问数</div>
              <div class="function-desc">自然语言查询数据</div>
            </div>
            <div class="function-item" @click="goTo('/skill/list')">
              <el-icon size="40" color="#E6A23C"><Tools /></el-icon>
              <div class="function-name">AI技能</div>
              <div class="function-desc">管理AI技能</div>
            </div>
            <div class="function-item" @click="goTo('/employee/list')">
              <el-icon size="40" color="#F56C6C"><User /></el-icon>
              <div class="function-name">数字员工</div>
              <div class="function-desc">创建智能员工</div>
            </div>
            <div class="function-item" @click="goTo('/data/crawler')">
              <el-icon size="40" color="#20B2AA"><DataLine /></el-icon>
              <div class="function-name">数据采集</div>
              <div class="function-desc">爬虫和ETL任务</div>
            </div>
            <div class="function-item" @click="goTo('/im/chat')">
              <el-icon size="40" color="#FF6347"><ChatDotRound /></el-icon>
              <div class="function-name">即时通讯</div>
              <div class="function-desc">实时聊天沟通</div>
            </div>
            <div class="function-item" @click="goTo('/admin/sensitive')">
              <el-icon size="40" color="#333"><Setting /></el-icon>
              <div class="function-name">系统管理</div>
              <div class="function-desc">系统配置管理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :md="8">
        <el-card class="quick-actions">
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <el-list>
            <el-list-item>
              <div class="quick-item">
                <span>快速开始NL2SQL查询</span>
                <el-button type="primary" text @click="goTo('/nl2sql/query')">开始查询</el-button>
              </div>
            </el-list-item>
            <el-list-item>
              <div class="quick-item">
                <span>创建数字员工</span>
                <el-button type="primary" text @click="goTo('/employee/list')">创建</el-button>
              </div>
            </el-list-item>
            <el-list-item>
              <div class="quick-item">
                <span>添加AI模型</span>
                <el-button type="primary" text @click="goTo('/model/list')">添加</el-button>
              </div>
            </el-list-item>
          </el-list>
        </el-card>
        
        <el-card class="system-info" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          <div class="info-item">
            <span class="info-label">系统版本：</span>
            <span class="info-value">v1.0.0</span>
          </div>
          <div class="info-item">
            <span class="info-label">框架：</span>
            <span class="info-value">Vue 3 + FastAPI</span>
          </div>
          <div class="info-item">
            <span class="info-label">开发模式：</span>
            <span class="info-value">4人4天敏捷开发</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

const goTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.welcome-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.welcome-card h2 {
  margin: 0 0 10px;
  font-size: 24px;
}

.welcome-card p {
  margin: 0;
  opacity: 0.9;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-content {
  position: relative;
  z-index: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

.stat-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 48px;
  opacity: 0.15;
}

.card-header {
  font-weight: 600;
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.function-item {
  padding: 20px;
  text-align: center;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.function-item:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
  transform: translateY(-2px);
}

.function-name {
  margin-top: 8px;
  font-weight: 600;
  color: #333;
}

.function-desc {
  margin-top: 4px;
  font-size: 12px;
  color: #999;
}

.quick-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #666;
  font-size: 14px;
}

.info-value {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}
</style>