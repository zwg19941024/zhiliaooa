<script setup name="frame">
import {ref,reactive,computed} from 'vue'
import {Expand,Fold,UserFilled} from '@element-plus/icons-vue'
import {useAuthStore} from '@/stores/auth'
import {useRoute,useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import http from '@/api/http.js'

let authStore=useAuthStore()
let router=useRouter()


let isCollapse=ref(false)
let dialogVisible=ref(false)
let resetPwdform=reactive({
    uid:'',
    oldpwd:'',
    newpwd1:'',
    newpwd2:'',
})
let formTag=ref()

let rules=reactive({
    oldpwd:[
        {required:true,message:'密码不能为空',trigger:'blur'},
        {min:6,max:12,message:'密码6-20位',trigger:'blur'},
    ],
    newpwd1:[
        {required:true,message:'密码不能为空',trigger:'blur'},
        {min:6,max:12,message:'密码6-20位',trigger:'blur'},
    ],
    newpwd2:[
        {required:true,message:'密码不能为空',trigger:'blur'},
        {min:6,max:12,message:'密码6-20位',trigger:'blur'},
    ]
})


let asideWidth=computed(()=>{
    if(isCollapse.value){
        return "64px"
    }
    return "250px"
})

const logout=()=>{  
    authStore.logout();
    router.push({name:"login"})
}

const changePassword=()=>{
    resetPwdform.oldpwd=''
    resetPwdform.newpwd1=''
    resetPwdform.newpwd2=''  
    dialogVisible.value=true
}

const resetPassword=()=>{
    formTag.value.validate(async(valid,fields)=>{
        if (!valid){
            ElMessage.error('填入信息错误')
            return 
        }
        try{
            resetPwdform.uid=authStore.user.uid
            await http.post('/auth/resetpwd',resetPwdform)
            dialogVisible.value=false
            ElMessage.success('密码修改成功')
        }
        catch(detail){
            ElMessage.error(detail)
        }
    })  
}

</script>

<template>
    <el-container class="container">
        <el-aside class="aside" :width="asideWidth">
            <router-link to="/" class="brand">管理<span v-show="!isCollapse">系统</span></router-link>
            <el-menu :router="true" active-text-color="#ffd04b" background-color="#343a40" class="el-menu-vertical-demo"
                default-active="1" text-color="#fff" :collapse="isCollapse" :collapse-transition="false" >
                <!-- 正式的内容 -->
                <!-- 首页 -->
                <el-menu-item index="1">
                    <el-icon><HomeFilled /></el-icon>
                    <span>首页</span>
                </el-menu-item>
                <!-- 考勤管理     -->
                <el-sub-menu index="2">
                    <template #title>
                        <el-icon><Checked /></el-icon>
                        <span>考勤管理</span>
                    </template>
                    <el-menu-item index="2-1" :route="{name: 'myabsent'}"><el-icon><UserFilled /></el-icon>个人考勤</el-menu-item>
                    <el-menu-item index="2-2" :route="{name: 'subabsent'}"><el-icon><User /></el-icon>下属考勤</el-menu-item>
                </el-sub-menu>
                <!-- 通知管理     -->
                <el-sub-menu index="3">
                    <template #title>
                        <el-icon><BellFilled /></el-icon>
                        <span>通知管理</span>
                    </template>
                    <el-menu-item index="3-1"><el-icon><CirclePlusFilled /></el-icon>发布通知</el-menu-item>
                    <el-menu-item index="3-2"><el-icon><List /></el-icon>通知列表</el-menu-item>
                </el-sub-menu>
                <!-- 员工管理     -->
                <el-sub-menu index="4">
                    <template #title>
                        <el-icon><Avatar /></el-icon>
                        <span>员工管理</span>
                    </template>
                    <el-menu-item index="4-1"><el-icon><CirclePlusFilled /></el-icon>新增员工</el-menu-item>
                    <el-menu-item index="4-2"><el-icon><List /></el-icon>员工列表</el-menu-item>
                </el-sub-menu>
                <!-- 模型管理     -->
                <el-sub-menu index="5">
                    <template #title>
                        <el-icon><BellFilled /></el-icon>
                        <span>模型管理</span>
                    </template>
                    <el-menu-item index="5-1"><el-icon><Files /></el-icon>模型列表</el-menu-item>
                </el-sub-menu>

            </el-menu>
        </el-aside>

        <el-container>
            <el-header class="header">
                <!-- 左边     -->
                <div class="left-header">
                    <el-button :icon="isCollapse ? Expand : Fold" @click="isCollapse = !isCollapse"/>
                </div>
                <!-- 右边     -->   
                <el-dropdown>
                    <span class="el-dropdown-link">
                        <el-avatar :size="30" :icon="UserFilled" />
                        <span style="margin-left: 10px;">[{{ authStore.user.department.name }}] {{authStore.user.realname}} </span>
                        <el-icon class="el-icon--right">
                            <arrow-down />
                        </el-icon>
                    </span>
                    <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="changePassword">修改密码</el-dropdown-item>
                        <el-dropdown-item divider @click="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-header>
            <el-main class="main">
                <RouterView></RouterView>
            </el-main>
        </el-container>
    </el-container>
    
    <!-- 修改密码 -->
    <el-dialog v-model="dialogVisible" title="修改密码" width="300px">
    <el-form :model="resetPwdform" :rules='rules' ref='formTag'>
      <el-form-item label="旧密码" prop='oldpwd' >
        <el-input v-model="resetPwdform.oldpwd" autocomplete="off" />
      </el-form-item>
      <el-form-item label="新密码" prop='newpwd1'>
        <el-input v-model="resetPwdform.newpwd1" autocomplete="off" />
      </el-form-item>
      <el-form-item label="确认密码" prop='newpwd2'>
        <el-input v-model="resetPwdform.newpwd2" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="resetPassword">确认</el-button>
      </div>
    </template>
    </el-dialog>

</template>

<style scoped>
.container {
    height: 100vh;
    background-color: #f4f6f9;
}

.aside {
    background-color: #343a40;
    box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22) !important;
}

.aside .brand {
    color: #fff;
    text-decoration: none;
    border-bottom: 1px solid #434a50;
    background-color: #232631;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
}

.header {
    background-color: #ffffff;
    height: 60px;
    display: flex;
    border-bottom: 1px solid #e6e6e6;
    justify-content: space-between;
    align-items: center;
}

.header .el-dropdown-link {
    display: flex;
    align-items: center;
    
}

.main {
    background-color: #fff;
    box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22) !important;
}

.el-menu {
    border-right: none;
}



</style>
