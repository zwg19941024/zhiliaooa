<script setup name="OAPageHeader">
import { useRouter } from 'vue-router';

let props=defineProps({
    content:''
})

const router=useRouter()

//返回上一界面
const goBack=()=>{
    router.go(-1)
}


</script>

<template>
    <el-page-header @back="goBack" title="返回">
        <template #content>
            <span class="text-large font-600 mr-3"> {{props.content}} </span>
        </template>
    </el-page-header>

</template>

<style></style>
