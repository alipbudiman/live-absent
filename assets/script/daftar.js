import { Ajaxx } from "./ajax.js";
import { Functionn } from "./function.js"

const aj = new Ajaxx();
const fun = new Functionn();

const urlParams = new URLSearchParams(window.location.search);
const nim = urlParams.get('nim') ?? 0;
const passcode = urlParams.get('passcode') ?? "";

if (nim === null || nim === 0 || nim === undefined) {
    window.location.href = "/";
}
if (passcode === null || passcode === "" | passcode === undefined) {
    window.location.href = "/";
}

let data = {
    nama: "",
    nim: nim,
    prodi: "infa",
    tanggapan: "",
    bp: 0,
    setuju: false,
}

const nama = document.getElementById("nama");
nama.addEventListener("keyup", () => {
    const _nama = document.getElementById("nama").value;
    data.nama = _nama;
});
const prodi = document.getElementById("prodi");
prodi.addEventListener("click", () => {
    const _prodi = document.getElementById("prodi").value;
    data.prodi = _prodi;
    
})
const bp = document.getElementById("bp");
bp.addEventListener("keyup", () => {
    const _bp = document.getElementById("bp").value;
    data.bp = _bp;
});
const textarea = document.getElementById("my-textarea");
textarea.addEventListener("keyup", () => {
    const _textarea = document.getElementById("my-textarea").value;
    data.tanggapan = _textarea;
});

const checkbox = document.getElementById('check-detect');
checkbox.addEventListener('click', function () {
    if (checkbox.checked) {
        data.setuju = true;
    } else {
        data.setuju = false;
    }
});

const button = document.getElementById('my-button');
let paragraph = document.getElementById('notification-message');
button.addEventListener('click', function (event) {
    event.preventDefault();
    if (textarea.value.trim() === '') {
        fun.autoAppend()
        paragraph.textContent = 'tolong isi kolom tanggapan'
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else if (textarea.value.trim().length < 30) {
        fun.autoAppend()
        paragraph.textContent = 'tolong buat pesan minimal 30 karakter';
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else if (data.setuju === false) {
        fun.autoAppend()
        paragraph.textContent = 'tolong centang terlebih dahulu checkbox setuju';
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else if (data.nama === "" || data.bp === 0 || data.prodi === "") {
        fun.autoAppend()
        let warn = ""
        if (data.nama === "") {
            warn += "nama,"
        }
        if (data.bp === "") {
            warn += "tahun angkatan,"
        }
        if (data.prodi === "") {
            warn += "prodi"
        }
        paragraph.textContent = `tolong isi kolom ${warn} terlebih dahulu`;
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else if (data.bp > 2023 || data.bp < 2000) {
        fun.autoAppend()
        paragraph.textContent = `tolong masukan tahun angkatan dengan benar`;
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else {
        aj.postData(data.tanggapan, data.nama, data.nim, data.prodi, data.setuju, data.bp, passcode);
    }
});