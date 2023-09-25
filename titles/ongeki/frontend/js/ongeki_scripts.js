function deleteRival(rivalUserId){

    $(document).ready(function () {
        $.post("/game/ongeki/rival.delete",
        {
            rivalUserId
        },
        function(data,status){
            window.location.replace("/game/ongeki/")
        })
    });
}
function changeVersion(sel){

    $(document).ready(function () {
        $.post("/game/ongeki/version.change",
        {
            version: sel.value
        },
        function(data,status){
            window.location.replace("/game/ongeki/")
        })
    });
}
