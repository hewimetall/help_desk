app_v = new Vue({
  el: '#apps_chat',
  data() {
    return {
      info: null,
      testinfo: null,
      timer: null,
    };
  },
  mounted() {
    // повторить с интервалом 1 секунды
    this.timer = setInterval(this.updateT, 2000);
  },
  methods: {
    formSubmit(e){
        const form = e.target;
        fetch(form.action, {
          method: form.method,
          body: new FormData(form)
        })
      e.preventDefault();
    },
    updateT() {
      axios.get(document.location['href'] + "rest/", {
        headers: {
          'x-xsrf-token': this.getCookie('csrftoken'),
        },
      }).then(response => (this.info = response.data));

    },
    getCookie(name) {
      let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
      ));
      return matches ? decodeURIComponent(matches[1]) : undefined;
    }
  }
});


Vue.component('chat-messenge', {
  props: ['m'],
  template: `
   <div class="msg mb-3">
                        <div class="media-body p-3">
                            <div class="row">
                                <h5 class="media-heading">{{ m.name }}</h5>
                                <small class="pull-left time"><i class="fa fa-clock-o"></i> {{ m.created }}</small>
                            </div>
                            <div class="alert-dark p-3">
                                <div class="col-12 col-sm-6 col-md-8"><small class="col-sm-11"> {{ m.body }} </small>
                                </div>
                                <div class="col-6 col-md-4">{{ m.file }}</div>
                            </div>
                        </div>
                    </div>`
});
