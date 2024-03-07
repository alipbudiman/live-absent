export class Functionn {


    closeButton() {
        let btn = document.querySelector('.hide-button');
        btn.style.animation = 'dissolve 1s';
        btn.style.visibility = 'hidden';
        btn.style.animation = ''
    }

    appendButton() {
        let btn = document.querySelector('.hide-button');
        btn.style.animation = 'dissolve-reverse 1s';
        btn.style.visibility = 'visible';
    }

    autoAppend(){
        let notification = document.querySelector('.notification');
        notification.style.animation = 'dissolve-reverse 1s';
        notification.style.visibility = 'visible';
    }

    autoClose(){
        let notification = document.querySelector('.notification');
        notification.style.animation = 'dissolve 2s';
        setTimeout(() => {
            notification.style.visibility = 'hidden';
            notification.style.animation = ''
        }, 2000);
    }

    enAES(message,a1,a2,ch){
        const keyBytes = CryptoJS.enc.Utf8.parse(this.siJerry(ch).substring(a1,a2));
        const ivBytes = CryptoJS.enc.Utf8.parse('0000000000000000');
        const encrypted = CryptoJS.AES.encrypt(message, keyBytes, { iv: ivBytes });
        return encrypted.toString();
    }

    makeSplit3(message) {
        const myArray = message.split("|");
        return {a1: parseInt(myArray[1]), a2: parseInt(myArray[2])}
    }

    siJerry(ch) {
        const acumalakucing = ch.split("|");
        return acumalakucing[0]

    }

    GetEveryItemsinSession(data_list) {
        let structure = ""
        for (let i=0; i < data_list.length; i++) {
            if (data_list[i] === "ch") {
                structure += "ch,"
            } else if (data_list[i] === "rid") {
                structure += "rid,"
            }
        }
        return structure
    }
}