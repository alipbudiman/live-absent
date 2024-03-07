async function LoadMessage() {
    while (true) {
        try {
            const data = await $.ajax({
                url: "/checkall/load",
                type: "GET",
            });
            $("#place_for_xrc23a").html(data);
        } catch (error) {
            console.log(error)
            location.reload()
        }
        await new Promise(resolve => setTimeout(resolve, 4000));
    }
}

LoadMessage()

const import_doc = document.getElementById("import")
import_doc.addEventListener("click", ()=> {
    $.ajax({
        url: "/checkall/import",
        type: "POST",
        dataType: "json",
        success: function (response) {
            alert(response.message)
        },
        error: function (jqXHR, textStatus, errorThrown) {
            const err = `ERROR: ${jqXHR} | ${textStatus} | ${errorThrown}`;
            alert(err)
        }
    });
})

const create_cert = document.getElementById("cert")
create_cert.addEventListener("click", ()=> {
    $.ajax({
        url: "/checkall/cert",
        type: "POST",
        dataType: "json",
        success: function (response) {
            alert(response.message)
        },
        error: function (jqXHR, textStatus, errorThrown) {
            const err = `ERROR: ${jqXHR} | ${textStatus} | ${errorThrown}`;
            alert(err)
        }
    });
})

const button = document.getElementById("button")
button.addEventListener('click', () => {
    const passcode = document.getElementById("passcode").value;
    const access = document.getElementById("access").value;
    const commands = document.getElementById("commands").value;
    const consolelock = document.getElementById("consolelock").value;
    const lastattend = document.getElementById("lastattend").value;
    if (passcode !== "" || access !== "" || commands !== "" || consolelock !== "" || lastattend !== "") {
        $.ajax({
            url: "/checkall/change",
            type: "POST",
            dataType: "json",
            data: {
                "passcode": passcode,
                "access": access,
                "commands":commands,
                "consolelock":consolelock,
                "lastattend":lastattend,
            },
            success: function (response) {
                if (response.code === 201) {
                    alert(response.message);
                } else if (response.code === 202) {
                    alert(response.message);
                    window.location.replace("/checkall");
                } else {
                    window.location.replace("/checkall");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                const err = `ERROR: ${jqXHR} | ${textStatus} | ${errorThrown}`;
                alert(err)
            }
        });

    } else {
        alert("Nothing happen 😕")
    }
})