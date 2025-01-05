<script setup name="subabsent">
import OAPageHeader from '@/components/OAPageHeader.vue';
import { ref, reactive, onMounted } from 'vue';
import absentHttp from '@/api/absentHttp';
import {ElMessage} from 'element-plus' 
import http from '@/api/http.js'
import {useRoute,useRouter} from 'vue-router'
import timeFormatter from '@/utils/timeFormatter'


const router=useRouter()

let dialogFormVisible = ref(false)
let absents=ref([])

let absentForm = reactive({
    id:'',
    title: '',
    absent_type: '',
    date_range: [],
    request_content: '',
    response_content: '',
    status:1,
    requester_realname:'',
    index:0
})
let pagination=reactive({
    page:1,
    pageSize:10,
    total:0
})


let requester =ref('')

//请假表单
const onShowDialog =async (index) => {
    absentForm.index=index
    absentForm.title =absents.value[index].title
    absentForm.absent_type= absents.value[index].absent_type.name
    absentForm.date_range = [absents.value[index].start_date,absents.value[index].end_date]
    absentForm.request_content = absents.value[index].request_content
    absentForm.requester_realname=absents.value[index].requester.realname
    dialogFormVisible.value = true;

}

//上传更新请假单
const onSubmitAbsent =async () => {
    try{ 
        const absent = absents.value[absentForm.index]
        let data={
            status:absentForm.status,
            response_content:absentForm.response_content
        }
        await http.put('/absent/absent/'+absent.id,data)
        ElMessage.success('审核提交成功')
        dialogFormVisible.value = false
        getMyAbsents(pagination.page)
        }catch(detail){
        ElMessage.error(detail)
        }

}

//获取下属考勤
const getMyAbsents =async (page=1) => {
    try{
            let result = await http.get('/absent/absent?who=sub&page='+page)
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
        <OAPageHeader content="下属考勤"></OAPageHeader>
       
        <!-- 请假单列表 -->
        <el-card>
            <el-table :data="absents" style="width: 100%">
                <el-table-column prop="title" label="标题" width="180"   />
                <el-table-column prop="requester.realname" label="请假者" width="80"   />
                <el-table-column prop="absent_type.name" label="请假类型" width="80" />
                <el-table-column prop="request_content" label="请假原因" />
                <el-table-column label="发起时间" >
                    <template #default="scope">
                        {{timeFormatter.stringFromDate(scope.row.create_time)}}
                    </template>
                </el-table-column>
                <el-table-column prop="start_date" label="开始时间" />
                <el-table-column prop="end_date" label="结束时间" />
                <el-table-column label="状态">
                    <template #default="scope">
                        <el-tag v-if="scope.row.status==1" type="warning">待审批</el-tag>
                        <el-tag v-else-if="scope.row.status==2" type="success">审批通过</el-tag>
                        <el-tag v-else-if="scope.row.status==3" type="danger">审批拒绝</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="response_content" label="反馈意见" />
                <!-- 操作按钮 -->
                <el-table-column fixed="right" label="操作" min-width="120">
                    <template #default ="scope">
                        <el-button type="primary" v-if="scope.row.status==1" icon="Edit"  @click="onShowDialog(scope.$index)"/>
                        <el-button type="default" v-else >已处理</el-button>
                    </template>
                </el-table-column>
                
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


    <!-- 审批下属考勤表单 -->
    <el-dialog v-model="dialogFormVisible" title="审批请假" width="500">
        <el-form :model="absentForm" >
            <!-- 标题 -->
            <el-form-item label="标题" :label-width="100" prop='title' >
                <el-input v-model="absentForm.title" autocomplete="off" readonly disabled />
            </el-form-item>
            <!-- 请假类型 -->
            <el-form-item label="请假类型" :label-width="100">
                <el-input v-model="absentForm.absent_type" autocomplete="off" readonly disabled />
            </el-form-item>
            <!-- 请假日期 -->
            <el-form-item label="请假时间" :label-width="100" prop='date_range'>
                <el-date-picker readonly disabled v-model="absentForm.date_range" type="daterange" range-separator="到"
                    start-placeholder="起始日期" end-placeholder="结束日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
            </el-form-item>
            <!-- 请假申请人 -->
            <el-form-item label="请假者" :label-width="100">
                <el-input :value="absentForm.requester_realname" readonly disabled autocomplete="off" />
            </el-form-item>
            <!-- 请假理由 -->
            <el-form-item label="请假理由" :label-width="100" prop='request_content'>
                <el-input type="textarea" v-model="absentForm.request_content" readonly disabled autocomplete="off" />
            </el-form-item>
            <!-- 回复意见 -->
            <el-form-item label="回复意见" :label-width="100" prop='response_content'>
                <el-input type="textarea" v-model="absentForm.response_content"  autocomplete="off" />
            </el-form-item>
            <!-- 审批操作 -->
            <el-form-item label="是否同意请假" :label-width="100" prop='status'>
                <el-radio-group v-model="absentForm.status" size="large">
                    <el-radio-button  label="同意" value=2 />
                    <el-radio-button  label="拒绝" value=3 />
                </el-radio-group>
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
