const urlParams = new URLSearchParams(window.location.search);
const _status = urlParams.get('status');

if (_status === "notallowed") {
    alert("PASSCODE SALAH!!")
}

const button2 = document.getElementById('my-button2');
button2.addEventListener('click', function (event) {
    window.location.href = `/editdata`;
})

const button = document.getElementById("sendpin");
button.addEventListener('click',()=>{
    setTimeout(() => {
        const passcode = document.getElementById("passcode").value;
        window.location.href = `/authorize?passcode=${passcode}`;
    }, 1000);
} )