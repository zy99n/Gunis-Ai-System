import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/modules/auth/pages/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/modules/auth/pages/Register.vue'),
    meta: { title: '注册', requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/modules/dashboard/pages/Dashboard.vue'),
        meta: { title: '工作台', icon: 'House' }
      }
      // TODO: 以下模块页面文件尚未创建，暂时注释
      // {
      //   path: 'organization',
      //   name: 'Organization',
      //   meta: { title: '组织管理', icon: 'OfficeBuilding' },
      //   children: [
      //     {
      //       path: 'department',
      //       name: 'DepartmentManage',
      //       component: () => import('@/modules/organization/pages/DepartmentManage.vue'),
      //       meta: { title: '部门管理' }
      //     },
      //     {
      //       path: 'user',
      //       name: 'UserManage',
      //       component: () => import('@/modules/organization/pages/UserManage.vue'),
      //       meta: { title: '用户管理' }
      //     }
      //   ]
      // },
      // {
      //   path: 'model',
      //   name: 'Model',
      //   meta: { title: '模型管理', icon: 'Box' },
      //   children: [
      //     {
      //       path: 'list',
      //       name: 'ModelList',
      //       component: () => import('@/modules/model/pages/ModelList.vue'),
      //       meta: { title: '模型列表' }
      //     }
      //   ]
      // },
      // {
      //   path: 'nl2sql',
      //   name: 'NL2SQL',
      //   meta: { title: '智能问数', icon: 'MagicStick' },
      //   children: [
      //     {
      //       path: 'query',
      //       name: 'NL2SQLQuery',
      //       component: () => import('@/modules/nl2sql/pages/QueryPanel.vue'),
      //       meta: { title: '查询分析' }
      //     }
      //   ]
      // },
      // {
      //   path: 'skill',
      //   name: 'Skill',
      //   meta: { title: 'AI技能', icon: 'Tools' },
      //   children: [
      //     {
      //       path: 'list',
      //       name: 'SkillList',
      //       component: () => import('@/modules/skill/pages/SkillList.vue'),
      //       meta: { title: '技能管理' }
      //     }
      //   ]
      // },
      // {
      //   path: 'employee',
      //   name: 'Employee',
      //   meta: { title: '数字员工', icon: 'User' },
      //   children: [
      //     {
      //       path: 'list',
      //       name: 'EmployeeList',
      //       component: () => import('@/modules/employee/pages/EmployeeList.vue'),
      //       meta: { title: '员工管理' }
      //     }
      //   ]
      // },
      // {
      //   path: 'data',
      //   name: 'Data',
      //   meta: { title: '数据采集', icon: 'DataLine' },
      //   children: [
      //     {
      //       path: 'crawler',
      //       name: 'CrawlerList',
      //       component: () => import('@/modules/data/pages/CrawlerList.vue'),
      //       meta: { title: '爬虫任务' }
      //     },
      //     {
      //       path: 'etl',
      //       name: 'EtlPipeline',
      //       component: () => import('@/modules/data/pages/EtlPipeline.vue'),
      //       meta: { title: 'ETL流水线' }
      //     }
      //   ]
      // },
      // {
      //   path: 'im',
      //   name: 'IM',
      //   meta: { title: '即时通讯', icon: 'ChatDotRound' },
      //   children: [
      //     {
      //       path: 'chat',
      //       name: 'ChatRoom',
      //       component: () => import('@/modules/im/pages/ChatRoom.vue'),
      //       meta: { title: '聊天室' }
      //     }
      //   ]
      // },
      // TODO: 系统管理模块待开发，暂时注释
      // {
      //   path: 'admin',
      //   name: 'Admin',
      //   meta: { title: '系统管理', icon: 'Setting' },
      //   children: [
      //     {
      //       path: 'sensitive',
      //       name: 'SensitiveWords',
      //       component: () => import('@/modules/admin/pages/SensitiveWords.vue'),
      //       meta: { title: '敏感词管理' }
      //     },
      //     {
      //       path: 'audit',
      //       name: 'AuditLogs',
      //       component: () => import('@/modules/admin/pages/AuditLogs.vue'),
      //       meta: { title: '审计日志' }
      //     }
      //   ]
      // }
    ]
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/modules/error/pages/NotFound.vue'),
    meta: { title: '页面不存在', requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.title) {
    document.title = `${to.meta.title} - 企业智能协同平台`
  }

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router