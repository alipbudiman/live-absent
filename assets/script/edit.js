import { Ajaxx } from "./ajax.js";
import { Functionn } from "./function.js"

const aj = new Ajaxx();
const fun = new Functionn();



const button = document.getElementById('my-button');
let paragraph = document.getElementById('notification-message');
button.addEventListener('click', function (event) {
    const prodi = document.getElementById("prodi").value;
    const nim = document.getElementById("nim").value;
    event.preventDefault();
    if (prodi === "" || nim === "") {
        fun.autoAppend()
        let warn = ""
        if (prodi === "") {
            warn += "prodi"
        }
        if (nim === "") {
            warn += "nim"
        }
        paragraph.textContent = `tolong isi kolom ${warn} terlebih dahulu`;
        setTimeout(() => {
            fun.autoClose()
        }, 2000);
    } else {
        console.log(nim, prodi)
        aj.editData(nim, prodi);
    }
});

