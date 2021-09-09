var baseurl = 'http://127.0.0.1:8000/';

var app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data : {
        csrf: null,
        user_name: [],
        task: {title: ''},
        updates: [],
        notices: [],
        lessons: [],
        office_hours: [],
        date: {day:''}, 
        maxDate: new Date().toISOString().split('T')[0],
        
    },

    computed:{
        
        filterNoticesById: function(notice_id){
                return this.notices.filter(notice => !notice.id.indexOf(notice_id))    
        },
        
    },

    methods: {
        
        async getCsrfToken(){
            if (this.csrf == null){
                var response = await fetch(baseurl + 'csrf');
                var data = await response.json();
                this.csrf = data.csrf_token;
            };
            return this.csrf;
        },  
        
        async getUser(){
            var  usern = await fetch(baseurl + 'getuser',
                {
                    method: 'get',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                }
            );
            this.user_name = await usern.json();
        }, 
        
        async getUpdates(){
            await fetch(baseurl + 'getupdates',
                {
                    method: 'post',
                    headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': await this.getCsrfToken()
                    },
                    body: JSON.stringify(this.date)
                }
            );
            
            var response = await this.loadUpdates();
            this.updates = await response.json()
        },

        async loadUpdates(){
            await this.getUser();
            var response = await fetch(baseurl + 'loadupdates',
                {
                    method: 'post',
                    headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': await this.getCsrfToken()
                    },
                    body: JSON.stringify(this.date)
                }
            );
            this.updates = await response.json()
            
            
        },
        async hide(element){
            
            await fetch(baseurl + 'hide',
            { method: 'post',
              headers: {
                  'Content-Type': 'application/json',
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': await this.getCsrfToken()
              },
              body: JSON.stringify(element)
            });
            await this.loadUpdates()
                        
        },

        async retrive(element){
            
            await fetch(baseurl + 'retrive',
            { method: 'post',
              headers: {
                  'Content-Type': 'application/json',
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': await this.getCsrfToken()
              },
              body: JSON.stringify(element)
            });
            await this.loadUpdates()
                        
        }, 
        
        

    },
    async created(){
        await this.getUpdates();
        
    }
})