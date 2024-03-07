import { Ajaxx } from "./ajax.js";
import { Functionn } from "./function.js"

const aj = new Ajaxx();
const fun = new Functionn();

const urlParams = new URLSearchParams(window.location.search);
const passcode = urlParams.get('passcode');

if (passcode === null || nim === "" || nim === undefined) {
    window.location.href = "/";
}

const button = document.getElementById('my-button');
button.addEventListener('click', function (event) {
    event.preventDefault();
    fun.autoAppend()
    const _nim = document.getElementById("nim").value;
    if (_nim === "") {
        paragraph.textContent = `tolong isi kolom ${warn} terlebih dahulu`;
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else {
        aj.verifyData(_nim, passcode);
    }
});

