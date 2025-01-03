import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  let _user =ref()
  let _token =ref()

  function setUserToken(user,token){
    //保存到对象
    _user.value = user
    _token.value = token
    //保存在硬盘上
    localStorage.setItem('OA_USER_KEY',JSON.stringify(user))
    localStorage.setItem('OA_TOKEN_KEY',token)
  } 

  function logout(){
    _user.value = null  
    _token.value = null
    localStorage.removeItem('OA_USER_KEY')
    localStorage.removeItem('OA_TOKEN_KEY')
  }

  let user=computed(()=>{
    if(_user.value){
      return _user.value
    }
    return localStorage.getItem('OA_USER_KEY')?JSON.parse(localStorage.getItem('OA_USER_KEY')):null
  })
  let token=computed(()=>{
    if(_token.value){
      return _token.value
    }
    return localStorage.getItem('OA_TOKEN_KEY')?localStorage.getItem('OA_TOKEN_KEY'):null
  })

  let is_logined = computed(() => {
    if(user.value && token.value){
      return true;
    }
    return false;
  })

  
  

  return { user,token,setUserToken,logout,is_logined }
})
