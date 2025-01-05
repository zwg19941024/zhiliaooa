<script setup name="myabsent">
import OAPageHeader from '@/components/OAPageHeader.vue';
import { ref, reactive, onMounted } from 'vue';
import absentHttp from '@/api/absentHttp';
import {ElMessage} from 'element-plus' 
import http from '@/api/http.js'
import {useRoute,useRouter} from 'vue-router'
import timeFormatter from '@/utils/timeFormatter'

const router=useRouter()

let absents=ref([])
let dialogFormVisible = ref(false)
let absentForm = reactive({
    title: '',
    absent_type_id: 1,
    date_range: [],
    request_content: '',
})
let pagination=reactive({
    page:1,
    pageSize:10,
    total:0
})

let absentFormTag = ref()
let absent_type = ref([])
let responder =ref('')

let rules=reactive({
    title:[
        {required:true,message:'请输入标题',trigger:'blur'},
    ],
    request_content:[
        {required:false,message:'',trigger:'blur'},
        {max:300,message:'超过300字符了',trigger:'blur'},
    ],
    date_range:[
        {required:true,message:'日期不能为空',trigger:'blur'},
    ]
})

const onShowDialog =async () => {
    absentForm.title = ''
    absentForm.absent_type_id = 1
    absentForm.date_range = []
    absentForm.request_content = ''
    dialogFormVisible.value = true;

    responder.value=await absentHttp.getResponder()
    absent_type.value=await absentHttp.getAbsentTypes()
}

//提交请假单
const onSubmitAbsent =async () => {
    absentFormTag.value.validate(async(valid,fields)=>{
        if (!valid){
            ElMessage.error('填入信息错误')
            return 
        }
        try{
            let data={
                title:absentForm.title,
                absent_type_id:absentForm.absent_type_id,
                start_date:absentForm.date_range[0],
                end_date:absentForm.date_range[1],
                request_content:absentForm.request_content
            }
            await http.post('/absent/absent',data)
            ElMessage.success('请假单提交成功')
            dialogFormVisible.value = false
            getMyAbsents(pagination.page)
        }
        catch(detail){
            ElMessage.error(detail)
        }
    })  
}

//获取个人考勤
const getMyAbsents =async (page=1) => {
    try{
            let result = await http.get('/absent/absent?who=my&page='+page)
            absents.value=result.results
            pagination.total=result.count
            pagination.page=page
        }
        catch(detail){
            ElMessage.error(detail)
        }

}

onMounted( async () => {
    try{
        await getMyAbsents()
    }catch(detail){
        ElMessage.error(detail)
    }
})


</script>

<template>
    <el-space direction="vertical" style="width: 100%" fill :size="20">
        <OAPageHeader content="个人考勤"></OAPageHeader>
        <el-card style="text-align: right;">
            <el-button @click="onShowDialog" type="primary"><el-icon>
                    <Plus />
                </el-icon > 发起考勤</el-button>
        </el-card>

        <!-- 请假单列表 -->
        <el-card>
            <el-table :data="absents" style="width: 100%">
                <el-table-column prop="title" label="标题" width="180" />
                <el-table-column prop="absent_type.name" label="请假类型" width="180" />
                <el-table-column prop="request_content" label="请假原因" />
                <el-table-column label="发起时间" >
                    <template #default="scope">
                        {{timeFormatter.stringFromDate(scope.row.create_time)}}
                    </template>
                </el-table-column>
                <el-table-column prop="start_date" label="开始时间" />
                <el-table-column prop="end_date" label="结束时间" />
                <el-table-column prop="responder.realname" label="审批人" />
                <el-table-column label="状态">
                    <template #default="scope">
                        <el-tag v-if="scope.row.status==1" type="warning">待审批</el-tag>
                        <el-tag v-else-if="scope.row.status==2" type="success">审批通过</el-tag>
                        <el-tag v-else-if="scope.row.status==3" type="danger">审批拒绝</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="response_content" label="反馈意见" />
            </el-table>
            <!-- 分页 -->
            <template #footer>
                <el-pagination background layout="prev, pager, next" 
                    :total="pagination.total" 
                    :page-size="pagination.pageSize"
                    v-model:current-page="pagination.page" 
                    @current-change="getMyAbsents"/>
            </template>

        </el-card>

    </el-space>

    <!-- 发起考勤的表单跳出页 -->
    <el-dialog v-model="dialogFormVisible" title="发起请假" width="500">
        <el-form :model="absentForm" :rules='rules' ref='absentFormTag'>
            <!-- 标题 -->
            <el-form-item label="标题" :label-width="100" prop='title'>
                <el-input v-model="absentForm.title" autocomplete="off" />
            </el-form-item>
            <!-- 请假类型 -->
            <el-form-item label="请假类型" :label-width="100">
                <el-select  v-model="absentForm.absent_type_id" placeholder="请选择请假类型">
                    <el-option v-for="item in absent_type" :label="item.name" :value="item.id" :key="item.name"/>
                </el-select>
            </el-form-item>
            <!-- 请假日期 -->
            <el-form-item label="请假时间" :label-width="100" prop='date_range'>
                <el-date-picker v-model="absentForm.date_range" type="daterange" range-separator="到"
                    start-placeholder="起始日期" end-placeholder="结束日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
            </el-form-item>
            <!-- 请假审批人 -->
            <el-form-item label="审批人" :label-width="100">
                <el-input :value="responder.realname==''?'无':responder.realname" readonly disabled autocomplete="off" />
            </el-form-item>
            <!-- 请假理由 -->
            <el-form-item label="请假理由" :label-width="100" prop='request_content'>
                <el-input type="textarea" v-model="absentForm.request_content" autocomplete="off" />
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="onSubmitAbsent">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>
    



</template>

<style scoped>
.el-pagination {
    justify-content: center;
}
.el-space :deep(.el-space__item){
    width: 100%;
}
</style>
