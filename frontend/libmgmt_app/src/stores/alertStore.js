import { defineStore } from "pinia";
import { toast } from "vue3-toastify";
import "../../node_modules/vue3-toastify/dist/index.css";

export const useAlertStore = defineStore('alert', () => {

    function success(message) {
        toast(message, {
            "theme": "colored",
            "type": "success",
            "position": "top-center",
            "autoClose": 2000,
            "hideProgressBar": true,
            "dangerouslyHTMLString": true
        })
    }

    function error(message){
        toast(message, {
            "theme": "colored",
            "type": "error",
            "position": "top-center",
            "autoClose": 2000,
            "hideProgressBar": true,
            "dangerouslyHTMLString": true
        })
    }

    function warning(message){
        toast(message, {
            "theme": "colored",
            "type": "warning",
            "position": "top-center",
            "autoClose": 2000,
            "hideProgressBar": true,
            "dangerouslyHTMLString": true
        })
    }

    function info(message){
        toast(message, {
            "theme": "colored",
            "type": "info",
            "position": "top-center",
            "autoClose": 2000,
            "hideProgressBar": true,
            "dangerouslyHTMLString": true
        })
    }

    return {
        success,
        error,
        warning,
        info
    }
});