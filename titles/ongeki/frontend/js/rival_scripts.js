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
