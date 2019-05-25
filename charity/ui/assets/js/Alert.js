Alert = (function () {
    var self = {};

    self.loaderObj = null;

    self.animation = function () {
        let anims = [
            "https://media1.tenor.com/images/75643fee47adf65a46b50261be687697/tenor.gif?itemid=7830200",
            "https://cdn.dribbble.com/users/255512/screenshots/2192065/animation.gif",
            "https://cdn.dribbble.com/users/279765/screenshots/1918018/loadinganimation.gif",
            "https://cdn.dribbble.com/users/563824/screenshots/3633228/untitled-5.gif",
            "https://mir-s3-cdn-cf.behance.net/project_modules/disp/b6e0b072897469.5bf6e79950d23.gif",
            "https://createwebsite.net/wp-content/uploads/2015/09/Loader1.gif",
        ]
        return anims[Math.floor(Math.random() * anims.length)]
    }

    self.Loader = function () {
        let app = self;
        self.loaderObj = swal({
            title: "Please Wait",
            imageUrl: app.animation(),
            imageAlt: "Loader",
            backdrop: `
          rgba(23, 24, 33, 0.81)
        `,
            timer: 8000,
            allowOutsideClick: false,
            showConfirmButton: false
        }).catch(swal.noop);
    };

    self.StopLoader = function () {
        swal({
            timer: 0.1,
            showConfirmButton: false,
            allowOutsideClick: false
        }).catch(swal.noop);
    };

    self.Info = function (msg) {
        swal({
            title: "<strong>Info</strong>",
            type: "info",
            html: "<pre>" + msg + "</pre>"
        }).catch(swal.noop);
    };

    return self;
})();