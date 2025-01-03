import axios from 'axios'
import { useAuthStore } from "@/stores/auth";

class Http{
    constructor(){
        this.instance = axios.create({
            //可能出错
            baseURL: import.meta.env.VITE_BASE_URL,
            timeout: 6000,
        });

        this.instance.interceptors.request.use((config) => {
            const authStore = useAuthStore()
            const token = authStore.token
            if(token){
                config.headers.Authorization = "JWT " + token
            }
            return config
        })
    }   
    post(path, data){
        return new Promise(async (resolve, reject) => {
            try{
                let result = await this.instance.post(path, data)
                resolve(result.data);
            }catch(err){
                let detail = err.response.data.detail;
                reject(detail)
            }
        })
    }

    get(path, params){
        return new Promise(async (resolve, reject) => {
            try{
                let result = await this.instance.get(path, params)
                resolve(result.data)
            }catch(err){
                let detail = err.response.data.detail;
                reject(detail)
            }
        })
    }

    put(path, data){
        return new Promise(async (resolve, reject) => {
            try{
                let result = await this.instance.put(path, data)
                resolve(result.data);
            }catch(err){
                let detail = err.response.data.detail;
                reject(detail)
            }
        })
    }
}


export default new Http()