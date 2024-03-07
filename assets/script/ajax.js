import { Functionn } from "./function.js"

export class Ajaxx extends Functionn {
    constructor() {
        super();
        this.data_type = "json";
    }

    autoClose() {
        super.autoClose();
    }

    autoAppend() {
        super.autoAppend();
    }

    editData(nim, prodi) {
        let send_to = "/editdata";
        this.autoAppend();
        let notification = document.querySelector('.notification');
        let paragraph = document.getElementById('notification-message');
        paragraph.textContent = 'Proses edit prodi . . .';
        $.ajax({
            url: send_to,
            type: "POST",
            dataType: this.data_type,
            data: {
                "nim": nim.toString(),
                "prod": prodi,
            },
            success: function (response) {
                // Handle the server response
                paragraph.textContent = response.message;
                setTimeout(() => {
                    notification.style.animation = 'dissolve 2s';
                    setTimeout(() => {
                        notification.style.visibility = 'hidden';
                        notification.style.animation = '';
                        notification.style.color = 'cyan'
                    }, 2000);
                }, 2000);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Handle errors
                notification.style.color = 'red'
                notification.style.visibility = 'visible';
                paragraph.textContent = 'Error:(' + textStatus + ": " + errorThrown + ")";
                setTimeout(() => {
                    notification.style.animation = 'dissolve 5s';
                    setTimeout(() => {
                        notification.style.visibility = 'hidden';
                        notification.style.animation = '';
                    }, 5000);
                }, 5000);
                notification.style.color = 'white'
                let btn = document.querySelector('.hide-button');
                btn.style.animation = 'dissolve-reverse 1s';
                btn.style.visibility = 'visible';
            }
        });
    }

    verifyData(nim, passcode) {
        let send_to = `/authorize?passcode=${passcode}`;
        this.autoAppend();
        let notification = document.querySelector('.notification');
        let paragraph = document.getElementById('notification-message');
        paragraph.textContent = 'Validasi sedang di proses . . .';
        $.ajax({
            url: send_to,
            type: "POST",
            dataType: this.data_type,
            data: {
                "nim": nim.toString(),
            },
            success: function (response) {
                // Handle the server response
                if (response.code === 200) {
                    setTimeout(() => {
                        notification.style.animation = 'dissolve 2s';
                        setTimeout(() => {
                            notification.style.visibility = 'hidden';
                            notification.style.animation = '';
                            notification.style.color = 'cyan'
                        }, 2000);
                    }, 2000);
                    window.location.replace("/success?protocol_id=" + response.return.data.uuid);
                } else if (response.code === 202) {
                    setTimeout(() => {
                        notification.style.animation = 'dissolve 2s';
                        setTimeout(() => {
                            notification.style.visibility = 'hidden';
                            notification.style.animation = '';
                            notification.style.color = 'cyan'
                        }, 2000);
                    }, 2000);
                    window.location.replace(`/daftar?passcode=${passcode}&nim=${nim}`);
                } else {
                    paragraph.textContent = response.return.message;
                    setTimeout(() => {
                        notification.style.animation = 'dissolve 2s';
                        setTimeout(() => {
                            notification.style.visibility = 'hidden';
                            notification.style.animation = '';
                            notification.style.color = 'cyan'
                        }, 2000);
                    }, 2000);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Handle errors
                notification.style.color = 'red'
                notification.style.visibility = 'visible';
                paragraph.textContent = 'Error:(' + textStatus + ": " + errorThrown + ")";
                setTimeout(() => {
                    notification.style.animation = 'dissolve 5s';
                    setTimeout(() => {
                        notification.style.visibility = 'hidden';
                        notification.style.animation = '';
                    }, 5000);
                }, 5000);
                notification.style.color = 'white'
                let btn = document.querySelector('.hide-button');
                btn.style.animation = 'dissolve-reverse 1s';
                btn.style.visibility = 'visible';
            }
        });
    }

    postData(tanggapan, nama, nim, prod, setuju, bp, passcode) {
        let send_to = `/daftar?passcode=${passcode}`;
        this.autoAppend();
        let notification = document.querySelector('.notification');
        let paragraph = document.getElementById('notification-message');
        paragraph.textContent = 'Mencoba mengirim pesan . . .';
        $.ajax({
            url: send_to,
            type: "POST",
            dataType: this.data_type,
            data: {
                "nim": nim.toString(),
                "nama": nama,
                "tanggapan": tanggapan,
                "prod": prod,
                "setuju": setuju,
                "bp": bp.toString(),
            },
            success: function (response) {
                // Handle the server response
                if (response.code === 200) {
                    console.log(response)
                    setTimeout(() => {
                        notification.style.animation = 'dissolve 2s';
                        setTimeout(() => {
                            notification.style.visibility = 'hidden';
                            notification.style.animation = '';
                            notification.style.color = 'cyan'
                        }, 2000);
                    }, 2000);
                    window.location.replace("/success?protocol_id=" + response.return.data.uuid);
                } else {
                    paragraph.textContent = response.return.message;
                    setTimeout(() => {
                        notification.style.animation = 'dissolve 2s';
                        setTimeout(() => {
                            notification.style.visibility = 'hidden';
                            notification.style.animation = '';
                            notification.style.color = 'cyan'
                        }, 2000);
                    }, 2000);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Handle errors
                notification.style.color = 'red'
                notification.style.visibility = 'visible';
                paragraph.textContent = 'Error:(' + textStatus + ": " + errorThrown + ")";
                setTimeout(() => {
                    notification.style.animation = 'dissolve 5s';
                    setTimeout(() => {
                        notification.style.visibility = 'hidden';
                        notification.style.animation = '';
                    }, 5000);
                }, 5000);
                notification.style.color = 'white'
                let btn = document.querySelector('.hide-button');
                btn.style.animation = 'dissolve-reverse 1s';
                btn.style.visibility = 'visible';
            }
        });
    }
}