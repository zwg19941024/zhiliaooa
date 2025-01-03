<script setup name="login">
import login_img from '@/assets/image/login.png'
import {reactive,ref} from 'vue'
import authHttp from '@/api/authHttp'
import {ElMessage} from 'element-plus'
import {useAuthStore} from '@/stores/auth'
import {useRouter} from 'vue-router'

const AuthStore=useAuthStore()
const router=useRouter()

let form =reactive({
    email:'',
    password:''
})

let imageCode=ref("")

const  onSubmit =async()=>{
    let pwdRgx = /^[0-9a-zA-Z_-]{6,20}/
    let emailRgx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9])+/
    if(!(emailRgx.test(form.email))){
        ElMessage.info('邮箱格式不满足！')
        return;
    }
    if(!(pwdRgx.test(form.password))){
        ElMessage.info("密码格式不满足！")
        return;
    }

    try{
        let data=await authHttp.login(form.email,form.password)
        let token=data.token;
        let user=data.user;
        AuthStore.setUserToken(user,token);
        //跳转首页
        router.push({name:"player"});
    }catch(detail){
        ElMessage.error(detail)
    }
}


</script>

<template>
<body>
    <div class="dowebok">
        <div class="container-login100">
            <div class="wrap-login100">
                <div class="login100-pic js-tilt" data-tilt>
                    <img :src="login_img" alt="IMG" />
                </div>

                <div class="login100-form validate-form">
                    <span class="login100-form-title"> 用户登陆 </span>
                    <div class="wrap-input100 validate-input">
                        <input class="input100" type="text" name="email" placeholder="邮箱" v-model="form.email" />
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
                            <i class="iconfont icon-fa-envelope" aria-hidden="true"></i>
                        </span>
                    </div>

                    <div class="wrap-input100 validate-input">
                        <input class="input100" type="password" name="password" placeholder="密码" v-model="form.password"/>
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
                            <i class="iconfont icon-fa-lock" aria-hidden="true"></i>
                        </span>
                    </div>
                    <!--图片验证 -->
                    <div class="wrap-input50 validate-input">
                        <input class="input50" type="text" name="image" placeholder="请输入验证码" v-model="imageCode"/>
                        <!-- <span class="focus-input100"></span> -->
                        <img class="fit-picture" src="" alt="图片无时文本"/>
                    </div>

                    <div class="container-login100-form-btn"> 
                        <button class="login100-form-btn" @click="onSubmit">
                            登陆
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</template>

<style scoped src="@/assets/css/login.css">
.fit-picture {
  width: 50px;
  height: 250px;
  border: 1px solid;
  margin: 5px;
}
</style>
